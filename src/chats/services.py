# services.py
import functools
import logging

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import GroupSettings, Chat, GroupSettingsHasUser, Message
from users.models import CustomUser

logger = logging.getLogger(__name__)


def check_to_admin(func):
    """Проверка на админа"""
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
    """Проверка на владельца"""
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

    def leave_user(self):
        self.chat.delete_user(self.user)

    @check_to_owner
    def delete_group(self):
        self.chat.delete()

    @staticmethod
    def get_or_create_group_settings(chat, title=None):
        if title:
            group_settings = GroupSettings.objects.get_or_create(chat=chat, title=title)[0]
        else:
            group_settings = GroupSettings.objects.get(chat=chat)
        return group_settings

    def create_group_chat(self, validated_data, title) -> Chat:
        group = Chat.objects.create(chat_type=validated_data['chat_type'],
                                    host=validated_data['host'])
        try:
            users = validated_data['current_users']
            users.append(validated_data['host'])
            group.add_users(users=validated_data['current_users'],
                            group_settings=self.get_or_create_group_settings(chat=group, title=title))
            return group
        except ValueError as error:
            print("Ошибка добавления пользователей: {}".format(error))
        return group


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

    def __init__(self, user):
        self.user = user

    def update_group_settings(self, validated_data, instance):
        """Изменяем данные группы - аватар, название"""

        group_settings_has_user = get_object_or_404(GroupSettingsHasUser, group_settings=instance.pk, user=self.user.pk)
        if group_settings_has_user.get_role_display() in ('admin', 'owner'):
            instance.avatar = validated_data.get('avatar', instance.avatar)
            instance.title = validated_data.get('title', instance.title)


class GroupSettingsHasUserService:

    def __init__(self, user):
        self.user = user

    def update_user_role(self, validated_data, instance):
        if validated_data.get('user', None) is None or validated_data.get('group_settings', None) is None:
            raise serializers.ValidationError('Нет значений пользователя и чата')
        if not isinstance(validated_data.get('user'), CustomUser) or \
                not isinstance(validated_data.get('group_settings'), GroupSettings):
            raise serializers.ValidationError('Не верный тип данных')

        group_settings_has_user = get_object_or_404(GroupSettingsHasUser,
                                                    group_settings=validated_data['group_settings'].pk,
                                                    user=self.user.pk)
        if group_settings_has_user:
            instance.change_role(self.user, validated_data['role'])
        else:
            raise serializers.ValidationError('Вы не состоите в группе!')


class MessageService:

    @staticmethod
    def delete_message(instance):
        instance.delete()

    @staticmethod
    def edit_message(validated_data, instance: Message):
        instance.text_content = validated_data.get('text_content', instance.text_content)
