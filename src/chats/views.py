from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
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


class GroupSettingsRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """Получаем данные о группе для отрисовки на интерфейсе,
        обновляем роли"""
    queryset = GroupSettings.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = GroupSettingsSerializer
    lookup_field = 'pk'
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def patch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = GroupSettingsSerializer(instance=instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            logger.error(error)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GroupSettingsHasUserView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = GroupSettingsHasUser.objects.all()
    serializer_class = GroupSettingsHasUserSerializer


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(),
                                user=self.request.data['user'],
                                group_settings=self.request.data['group_settings'])
        self.check_object_permissions(self.request, obj)
        return obj

    def patch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        except Exception as error:
            print(error)
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
            logger.error(f"Ошибка валидации:, {e.detail}")
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
            logger.error(f"Ошибка валидации:, {e.detail}")
            return Response(status=status.HTTP_400_BAD_REQUEST)
