from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField, SlugRelatedField

from .models import *

from users.models import CustomUser
import logging

logger = logging.getLogger(__name__)


class MessageSerializer(serializers.ModelSerializer):
    created_at_formatted = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = '__all__'

    def create(self, validated_data):
        return Message.objects.create(**validated_data)

    def get_created_at_formatted(self, obj: Message):
        return obj.created_at.strftime("%d-%m-%Y %H:%M:%S")

    def get_user(self, obj: Message):
        from users.serializers import UserDataOnChatSerializer
        return UserDataOnChatSerializer(obj.user).data


class ChatCardSerializer(serializers.ModelSerializer):
    """Отрисовка чатов в sidebar-е"""
    last_message = serializers.SerializerMethodField()
    current_users = serializers.SerializerMethodField()
    notifications = serializers.SerializerMethodField()
    host = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Chat
        fields = ('chat_type', 'host', 'current_users', 'last_message', 'pk', 'notifications')

    def get_last_message(self, obj: Chat):
        return MessageSerializer(obj.messages.order_by('created_at').last()).data

    def get_current_users(self, obj: Chat):
        from users.serializers import UserDataOnChatSerializer
        return UserDataOnChatSerializer(obj.current_users.all(), many=True).data

    def get_notifications(self, obj: Chat):
        user = self.context.get('user', None)
        if user is None:
            return None
        try:
            user_to_chat = UserToChat.objects.get(chat_id=obj.pk, user_id=user.pk)
            return user_to_chat.count_notifications
        except UserToChat.DoesNotExist:
            return None


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    current_users = serializers.SerializerMethodField()
    host = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Chat
        fields = ('messages', 'chat_type', 'host', 'current_users', 'pk')

    def create(self, validated_data):
        raise NotImplementedError()

    def get_current_users(self, obj: Chat):
        from users.serializers import UserDataOnChatSerializer
        return UserDataOnChatSerializer(obj.current_users.all(), many=True).data


class GroupChatSerializer(ChatSerializer):
    group_settings = serializers.SerializerMethodField()
    current_users = SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all(),
        many=True)

    class Meta(ChatSerializer.Meta):
        depth = 1
        fields = ChatSerializer.Meta.fields + ('group_settings',)

    def create(self, validated_data):
        return self.group_chat(validated_data)

    def get_group_settings(self, obj: Chat):

        group_settings = self.get_or_create_group_settings(chat=obj)
        return GroupSettingsSerializer(group_settings).data

    def get_or_create_group_settings(self, chat):
        title = self.context.get('title', None)
        if title:
            group_settings = GroupSettings.objects.get_or_create(chat=chat, title=title)[0]
        else:
            group_settings = GroupSettings.objects.get(chat=chat)

        return group_settings

    def group_chat(self, validated_data) -> Chat:
        group = Chat.objects.create(chat_type=validated_data['chat_type'],
                                    host=validated_data['host'])
        try:
            users = validated_data['current_users']
            users.append(validated_data['host'])
            group.add_users(users=validated_data['current_users'],
                            group_settings=self.get_or_create_group_settings(chat=group))
            return group
        except ValueError as error:
            print("Ошибка добавления пользователей: {}".format(error))
        return group


class PrivateChatSerializer(ChatSerializer):
    """Добавить сюда пользователя - собеседника"""
    current_users = SlugRelatedField(
        slug_field='username',
        queryset=CustomUser.objects.all(),
        many=True)

    class Meta(ChatSerializer.Meta):
        depth = 1
        fields = ChatSerializer.Meta.fields

    def create(self, validated_data):
        if len(validated_data['current_users']) == 1:
            return self.private_chat(validated_data)
        else:
            raise ValueError('error')


    @staticmethod
    def private_chat(validated_data) -> Chat:

        revert_chat = Chat.objects.filter(
            chat_type='P',
            host=validated_data['current_users'][0].pk,
            current_users=validated_data['host'].pk
        ).exists()

        cur_chat = Chat.objects.filter(
            chat_type='P',
            host=validated_data['host'].pk,
            current_users=validated_data['current_users'][0].pk,
        ).exists()

        if not revert_chat and not cur_chat:
            chat = Chat.objects.create(chat_type=validated_data['chat_type'], host=validated_data['host'])
            try:
                chat.add_users(users=validated_data['current_users'][0].pk)
                chat.add_users(users=validated_data['host'].pk)
                return chat
            except ValueError as error:
                print(f"Ошибка добавления пользователей: {error}")
                raise serializers.ValidationError({"detail": "Ошибка добавления пользователей."})
        else:
            raise serializers.ValidationError({"detail": "Чат уже существует."})


class GroupSettingsSerializer(serializers.ModelSerializer):
    """Чтобы выводить не пк users, нужно изменить"""

    class Meta:
        model = GroupSettings
        fields = '__all__'

