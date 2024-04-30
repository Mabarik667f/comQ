from typing import Dict, Any

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token

from .models import *


class UserShortDataSerializer(serializers.ModelSerializer):
    """Сериализатор для получения минимальных данных о пользователе"""

    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'img', 'status']


class UserInChatSerializer(serializers.ModelSerializer):
    """Сериализатор для получения данных о пользователе в чате"""

    class Meta:
        model = CustomUser
        fields = ['name', 'img']


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля"""

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'status', 'img']


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
