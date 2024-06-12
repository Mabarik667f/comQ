from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from users.models import CustomUser

from .models import Chat, Message, MessageContent, UserToChat
from .serializers import ChatSerializer, MessageSerializer
from users.serializers import UserProfileSerializer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """Connect to ws"""
        self.chat_pk = self.scope["url_route"]["kwargs"]["chat"]
        self.chat_group = f"chat_{self.chat_pk}"

        await self.add_user_to_chat(self.chat_pk)
        await self.channel_layer.group_add(self.chat_group, self.channel_name)

        chat: Chat = await self.get_chat()
        data = await self.get_serialized_data(ChatSerializer, chat)

        await self.accept()
        await self.send_json(content=data)


    async def leave_chat(self, chat):
        """Пользователь покидает чат"""
        await self.remove_user_from_chat(chat)

    async def join_chat(self, chat):
        """Пользователь присоединяется к чату"""
        await self.add_user_to_chat(chat)

    @database_sync_to_async
    def add_user_to_chat(self, chat):
        """Добавление пользователя в чат"""
        user: CustomUser = self.scope['user']
        if not user.current_chats.filter(pk=chat).exists:
            user.current_chats.add(Chat.objects.get(pk=chat))

    @database_sync_to_async
    def remove_user_from_chat(self, chat):
        """Удаление пользователя из чата"""
        user: CustomUser = self.scope['user']
        user.current_chats.remove(chat)

    @database_sync_to_async
    def get_chat(self):
        return Chat.objects.get(pk=self.chat_pk)

    @database_sync_to_async
    def get_serialized_data(self, serializer, pk):
        return serializer(pk).data

    @database_sync_to_async
    def current_users(self):
        chat = Chat.objects.get(pk=self.chat_pk)
        return [UserProfileSerializer(user).data for user in chat.current_users.all()]

    @database_sync_to_async
    def update_notifications(self):
        user_to_chat = UserToChat.objects.get(chat_id=self.chat_pk, user_id=self.scope['user'])
        user_to_chat.count_notifications = user_to_chat.count_notifications + 1
        user_to_chat.save()

    async def create_message(self, message):
        chat: Chat = await self.get_chat()
        content_type = await database_sync_to_async(MessageContent.objects.get_or_create)(
            name=MessageContent.TypeOfMessageContent.TEXT
        )
        new_message = await database_sync_to_async(Message.objects.create)(
            chat=chat,
            user=self.scope['user'],
            content_type=content_type[0],
            text_content=message
        )

        return await self.get_serialized_data(MessageSerializer, new_message)

    async def disconnect(self, close_code):
        """Disconect to ws"""
        await self.channel_layer.group_discard(self.chat_group, self.channel_name)

    # Receive message from WebSocket
    async def receive_json(self, content):
        new_message = await self.create_message(content['message'])
        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group, {"type": "chat.message",
                              "message": new_message}
        )

    async def chat_message(self, event):
        if self.scope['user'].pk != int(event['message']['user']['id']):
            await self.update_notifications()
        await self.send_json({"message": event['message']})