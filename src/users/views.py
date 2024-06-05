from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenBlacklistView, TokenRefreshView

from .serializers import *

USER: CustomUser = get_user_model()


class UserDataOnChatView(generics.RetrieveAPIView):
    """Получаем данные о пользователе в рамках чата"""
    serializer_class = UserDataOnChatSerializer
    authentication_classes = [JWTAuthentication]
    lookup_url_kwarg = "username"
    lookup_field = 'username'
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()


class UserDataView(generics.RetrieveAPIView):
    """Получение общих данных о пользователе для главной страницы:
        списка пользователей в чате
        статус
        id
        имя"""
    serializer_class = UserDataSerializer
    authentication_classes = [JWTAuthentication]
    lookup_url_kwarg = "user_id"
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    """Отображение данных пользователя в его профиле"""
    serializer_class = UserProfileSerializer
    lookup_url_kwarg = 'user_id'
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()


class MyObtainTokenPairView(TokenObtainPairView):
    """Вьюха для работы с jwt токеном авторизации с кастомными данными"""
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer: MyTokenObtainPairSerializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            refresh = RefreshToken.for_user(user)

            return Response({'refresh': str(refresh),
                             'access': str(refresh.access_token)},
                            status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    """Вьюха регистрации"""

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer: RegistrationSerializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class MyVerifyTokenView(TokenVerifyView):
    permission_classes = (AllowAny,)
    authentication_classes = [JWTAuthentication]


class MyTokenBlackListView(TokenBlacklistView):
    permission_classes = (AllowAny,)


class MyRefreshTokenView(TokenRefreshView):
    """
    """
