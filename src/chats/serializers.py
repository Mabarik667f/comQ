from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import PrimaryKeyRelatedField, SlugRelatedField

from .models import *

from users.models import CustomUser
import logging

from .services import GroupChatService, PrivateChatService, GroupSettingsService, GroupSettingsHasUserService

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
        many=True,
        required=False)

    class Meta(ChatSerializer.Meta):
        depth = 1
        fields = ChatSerializer.Meta.fields + ('group_settings',)
        extra_kwargs = {
            'chat_type': {'required': False},
        }

    def create(self, validated_data):
        service_obj = GroupChatService(user=self.context['user'], chat=None)
        title = self.context.get('title', None)
        return service_obj.create_group_chat(validated_data, title)

    def get_group_settings(self, obj: Chat):
        service_obj = GroupChatService(user=self.context['user'], chat=None)
        group_settings = service_obj.get_or_create_group_settings(chat=obj)
        return GroupSettingsSerializer(group_settings).data


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

    def update(self, instance: GroupSettings, validated_data):
        service_obj = GroupSettingsService(user=self.context.get('user'))
        service_obj.update_group_settings(validated_data, instance)
        instance.save()
        return instance


class GroupSettingsHasUserSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    group_settings = serializers.PrimaryKeyRelatedField(queryset=GroupSettings.objects.all())

    class Meta:
        model = GroupSettingsHasUser
        fields = "__all__"

    def update(self, instance: GroupSettingsHasUser, validated_data):

        service_obj = GroupSettingsHasUserService(user=self.context.get('user'))
        service_obj.update_user_role(validated_data, instance)
        instance.save()
        return instance
