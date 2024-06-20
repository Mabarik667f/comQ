from typing import Dict, Any

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token, RefreshToken

from .models import *
from chats.serializers import ChatCardSerializer, GroupSettingsHasUserSerializer

from .services import ProfileService
from chats.models import GroupSettingsHasUser, UserToChat, Chat, GroupSettings


class RelatedUsersSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['users', ]

    def get_users(self, obj: CustomUser):
        chat_ids = UserToChat.objects.filter(user_id=obj.pk).values('chat_id')
        users_to_exclude = (UserToChat.objects.filter(chat_id__in=chat_ids)
                            .exclude(user_id=obj.pk)
                            .values_list('user_id', flat=True)
                            .distinct())

        users = CustomUser.objects.filter(pk__in=users_to_exclude)

        return UserDataOnChatSerializer(users, many=True).data


class UserDataOnChatSerializer(serializers.ModelSerializer):
    """Получаем данные о пользователе в рамках чата"""
    is_online = serializers.SerializerMethodField()
    group_settings_has_user = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'img', 'status', 'is_online', 'group_settings_has_user']

    def get_is_online(self, obj: CustomUser):
        return obj.is_online()

    def get_group_settings_has_user(self, obj: CustomUser):
        chat = self.context.get('chat', None)
        if chat is not None:
            try:
                group_settings = GroupSettings.objects.get(chat=chat)
                group_has_user_settings = GroupSettingsHasUser.objects.get(user=obj, group_settings=group_settings)
                return GroupSettingsHasUserSerializer(group_has_user_settings, many=False).data
            except GroupSettings.DoesNotExist:
                return None
            except GroupSettingsHasUser.DoesNotExist:
                return None


class UserDataSerializer(serializers.ModelSerializer):
    """Сериализатор для получения общих данных о пользователе"""
    chats = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'img', 'status', 'chats']

    def get_chats(self, obj: CustomUser):
        chats = Chat.objects.filter(current_users=obj)
        return ChatCardSerializer(chats, many=True, context={'user': obj}).data


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля"""

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'status', 'img', 'email']

    def update(self, instance, validated_data):

        service_obj = ProfileService(user=self.context.get('user'))
        service_obj.update_profile_data(validated_data, instance)
        instance.save()
        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user: AuthUser) -> Token:
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['name'] = user.name
        return token

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except Exception as e:
            self.fail('bad_token')


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    email = serializers.EmailField(required=True,
                                   validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(required=True, min_length=8, write_only=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(required=True, min_length=8, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают!"})

        return attrs

    def create(self, validated_data):
        user: CustomUser = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['username']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
