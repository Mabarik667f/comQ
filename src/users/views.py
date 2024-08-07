from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework import generics
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import *

USER: CustomUser = get_user_model()


class RelatedUsersView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = RelatedUsersSerializer
    lookup_field = "username"
    lookup_url_kwarg = "username"

    def get_queryset(self):
        username = self.kwargs.get(self.lookup_url_kwarg)
        return CustomUser.objects.filter(username=username)


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
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer: UserProfileSerializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class MyObtainTokenPairView(TokenObtainPairView):
    """Вьюха для работы с jwt токеном авторизации с кастомными данными"""
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


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


class MyRefreshTokenView(TokenRefreshView):
    authentication_classes = [JWTAuthentication]


class LogoutView(APIView):

    permission_classes = (IsAuthenticated, )
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


