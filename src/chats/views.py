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


class GroupChatRetrieveDestroyView(generics.RetrieveDestroyAPIView):
    """Получаем данные о группе для отрисовки на интерфейсе"""
    queryset = Chat.objects.filter(chat_type="G")
    authentication_classes = [JWTAuthentication]
    serializer_class = GroupChatSerializer
    lookup_field = 'pk'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer: GroupChatSerializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.delete_group()
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class GroupChatUsersView(generics.GenericAPIView,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):

    queryset = Chat.objects.filter(chat_type="G")
    authentication_classes = [JWTAuthentication]
    serializer_class = GroupChatSerializer
    lookup_field = 'pk'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer: GroupChatSerializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        service_obj = GroupChatService(request.user, instance)
        service_obj.add_user(serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer: GroupChatSerializer = self.get_serializer(instance, data=request.data, patrial=True)
        serializer.is_valid(raise_exception=True)
        serializer.leave_user()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer: GroupChatSerializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        service_obj = GroupChatService(request.user, instance)
        service_obj.delete_user(serializer.validated_data)

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class GroupSettingsRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """Получаем данные о группе для отрисовки на интерфейсе,
        обновляем роли"""
    queryset = GroupSettings.objects.all()
    authentication_classes = [JWTAuthentication]
    serializer_class = GroupSettingsSerializer
    lookup_field = 'pk'
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def patch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
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
