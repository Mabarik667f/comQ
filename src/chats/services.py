# services.py
import functools
import logging

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import GroupSettings, Chat, GroupSettingsHasUser
from users.models import CustomUser

logger = logging.getLogger(__name__)


def check_to_admin(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        group_settings = self.get_group_settings()
        group_settings_has_user = get_object_or_404(GroupSettingsHasUser,
                                                    group_settings=group_settings,
                                                    user=self.user)
        if group_settings_has_user.get_role_display() in ('admin', 'owner'):
            return func(self, *args, **kwargs)
        else:
            logger.error('Вы не являетесь админом!')
            raise ValueError('Вы не являетесь админом!')

    return wrapper


def check_to_owner(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        group_settings = self.get_group_settings()
        group_settings_has_user = get_object_or_404(GroupSettingsHasUser,
                                                    group_settings=group_settings,
                                                    user=self.user)
        if group_settings_has_user.get_role_display() == 'owner':
            return func(self, *args, **kwargs)
        else:
            logger.error('Вы не являетесь владельцем!')
            raise ValueError('Вы не являетесь админом!')

    return wrapper


class GroupChatService:

    def __init__(self, user, chat):
        self.user = user
        self.chat = chat

    def get_group_settings(self):
        return get_object_or_404(GroupSettings, chat=self.chat)

    @check_to_admin
    def add_user(self, validated_data):
        group_settings = self.get_group_settings()
        self.chat.add_users(validated_data.get('current_users'), group_settings)

    @check_to_admin
    def delete_user(self, validated_data):
        del_user = validated_data.get('current_users')[0]
        if self.chat.host == del_user:
            raise ValueError("Вы не можете удалить владельца чата")
        else:
            self.chat.delete_user(del_user)

    def leave_user(self, validated_data):
        pass

    @check_to_owner
    def delete_group(self, validated_data):
        pass


class PrivateChatService:
    """Логика работы с приватными чатамм"""

    @staticmethod
    def create_private_chat(validated_data) -> Chat:

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


class GroupSettingsService:
    pass
