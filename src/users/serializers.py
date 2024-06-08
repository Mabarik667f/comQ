from typing import Dict, Any

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token, RefreshToken

from .models import *
from chats.serializers import ChatCardSerializer

from chats.models import Chat


class UserDataOnChatSerializer(serializers.ModelSerializer):
    """Получаем данные о пользователе в рамках чата"""

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'img', 'status']


class UserDataSerializer(serializers.ModelSerializer):
    """Сериализатор для получения общих данных о пользователе"""
    chats = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'img', 'status', 'chats']

    def get_chats(self, obj: CustomUser):
        chats = Chat.objects.filter(current_users=obj)
        return ChatCardSerializer(chats, many=True).data


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля"""

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'status', 'img', 'email']


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
