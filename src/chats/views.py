from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import *
from users.models import CustomUser
import logging

logger = logging.getLogger(__name__)


class ChatRetrieveView(generics.RetrieveAPIView):
    """Получаем данные о чате для отрисовки на интерфейсе"""
    queryset = Chat.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = ChatSerializer
    lookup_field = 'pk'


class GroupChatRetrieveView(generics.RetrieveAPIView):
    """Получаем данные о группе для отрисовки на интерфейсе"""
    queryset = Chat.objects.filter(chat_type="G")
    authentication_classes = [JWTAuthentication]
    serializer_class = GroupChatSerializer
    lookup_field = 'pk'


class GroupSettingsRetrieveView(generics.RetrieveAPIView):
    """Получаем данные о группе для отрисовки на интерфейсе"""
    queryset = GroupSettings.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = GroupSettingsSerializer
    lookup_field = 'pk'


class CreatePrivateChatView(APIView):
    """
    Создаем чат
    """
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = PrivateChatSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            print("Ошибка валидации:", e.detail)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class CreateGroupChatView(APIView):
    """
    Создаем чат
    """
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = GroupChatSerializer(data=request.data, context={'title': request.data['title']})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except serializers.ValidationError as e:
            print("Ошибка валидации:", e.detail)
            return Response(status=status.HTTP_400_BAD_REQUEST)
