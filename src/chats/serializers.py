from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import PrimaryKeyRelatedField, SlugRelatedField

from .models import *

from users.models import CustomUser
import logging

from .services import GroupChatService, PrivateChatService

logger = logging.getLogger(__name__)

"""Вынос логики во views и services"""


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
    host = PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), required=False)

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
        extra_kwargs = {
            'chat_type': {'required': False},
        }

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
            return PrivateChatService.create_private_chat(validated_data)
        else:
            raise ValueError('error')


class GroupSettingsSerializer(serializers.ModelSerializer):
    """Чтобы выводить не пк users, нужно изменить"""

    class Meta:
        model = GroupSettings
        fields = '__all__'

    def update(self, instance, validated_data):
        """Изменяем данные группы - аватат, название"""
        if 'avatar' in validated_data and instance.avatar != 'chat_avatars/default.jpg':
            instance.avatar.delete()

        user = self.context['user']
        group_settings_has_user = get_object_or_404(GroupSettingsHasUser, group_settings=instance.pk, user=user.pk)
        if group_settings_has_user.get_role_display() in ('admin', 'owner'):

            instance.avatar = validated_data.get('avatar', instance.avatar)
            instance.title = validated_data.get('title', instance.title)

        instance.save()

        return instance


class GroupSettingsHasUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    group_settings = serializers.PrimaryKeyRelatedField(queryset=GroupSettings.objects.all())

    class Meta:
        model = GroupSettingsHasUser
        fields = "__all__"

    def update(self, instance: GroupSettingsHasUser, validated_data):

        if validated_data.get('user', None) is None or validated_data.get('group_settings', None) is None:
            raise serializers.ValidationError('Нет значений пользователя и чата')
        if not isinstance(validated_data.get('user'), CustomUser) or \
                not isinstance(validated_data.get('group_settings'), GroupSettings):
            raise serializers.ValidationError('Не верный тип данных')

        user = self.context['user']
        group_settings_has_user = get_object_or_404(GroupSettingsHasUser,
                                                    group_settings=validated_data['group_settings'].pk,
                                                    user=user.pk)
        if group_settings_has_user:
            instance.change_role(user, validated_data['role'])
        else:
            raise serializers.ValidationError('Вы не состоите в группе!')

        instance.save()
        return instance
