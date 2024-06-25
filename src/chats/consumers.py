from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework.generics import get_object_or_404

from users.models import CustomUser

from .models import Chat, Message, MessageContent, UserToChat, GroupSettings
from .serializers import ChatSerializer, MessageSerializer, GroupSettingsSerializer
from users.serializers import UserProfileSerializer, UserDataOnChatSerializer
import logging

from .services import GroupChatService

logger = logging.getLogger("consumer")


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

    async def get_group_service(self):
        chat: Chat = await self.get_chat()
        return GroupChatService(user=self.scope['user'], chat=chat)

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
    def get_serialized_data(self, serializer, pk, *args, **kwargs):
        return serializer(pk, *args, **kwargs).data

    @database_sync_to_async
    def current_users(self):
        chat = Chat.objects.get(pk=self.chat_pk)
        return [UserProfileSerializer(user).data for user in chat.current_users.all()]

    @database_sync_to_async
    def update_notifications(self):
        user_to_chat = UserToChat.objects.get(chat_id=self.chat_pk, user_id=self.scope['user'])
        user_to_chat.count_notifications = user_to_chat.count_notifications + 1
        user_to_chat.save()

    @database_sync_to_async
    def get_group_settings(self):
        return get_object_or_404(GroupSettings, chat=Chat.objects.get(pk=self.chat_pk))

    async def create_message(self, message, system=False, reply=False):
        chat: Chat = await self.get_chat()
        content_type = await database_sync_to_async(MessageContent.objects.get_or_create)(
            name=MessageContent.TypeOfMessageContent.TEXT
        )
        new_message = await database_sync_to_async(Message.objects.create)(
            chat=chat,
            user=self.scope['user'],
            content_type=content_type[0],
            text_content=message,
            system=system,
            reply=reply
        )

        return await self.get_serialized_data(MessageSerializer, new_message)

    @staticmethod
    async def delete_message(message_id):
        message = await database_sync_to_async(Message.objects.get)(pk=message_id)
        await database_sync_to_async(message.delete)()

    async def edit_message(self, message_id, message_text, chat):
        message = await database_sync_to_async(Message.objects.get)(pk=message_id)
        serializer = await database_sync_to_async(MessageSerializer)(data={"text_content": message_text, "chat": chat})
        await database_sync_to_async(serializer.is_valid)(raise_exception=True)
        await database_sync_to_async(serializer.update)(instance=message, validated_data=serializer.validated_data)
        return await self.get_serialized_data(MessageSerializer, message)

    async def delete_user(self, user):
        user: CustomUser = await database_sync_to_async(CustomUser.objects.get)(username=user)
        service: GroupChatService = await self.get_group_service()
        await service.delete_user(deleted_user=user)
        serializer_data = await self.get_serialized_data(UserDataOnChatSerializer, user)
        message = await self.create_message(f"Пользователь {serializer_data['name']} был удален!", system=True)
        return serializer_data, message

    async def leave_user(self):
        service: GroupChatService = await self.get_group_service()
        await service.leave_user()
        serializer_data = await self.get_serialized_data(UserDataOnChatSerializer, self.scope['user'])
        message = await self.create_message(f"Пользователь {serializer_data['name']} покинул чат!", system=True)
        return serializer_data, message

    async def add_users(self, users):
        new_users = []
        messages = []
        service: GroupChatService = await self.get_group_service()
        chat: Chat = await self.get_chat()
        for user in users:
            user = user.get('value')
            user: CustomUser = await database_sync_to_async(CustomUser.objects.get)(username=user)
            await service.add_user(added_user=[user])
            await database_sync_to_async(user.refresh_from_db)()
            user_data = await self.get_serialized_data(UserDataOnChatSerializer, user,
                                                       context={"chat": chat})
            new_users.append(user_data)
            message = await self.create_message(f"Пользователь {user_data['name']} был добавлен!",
                                                system=True)
            messages.append(message)
        return new_users, messages

    async def delete_chat(self):
        service: GroupChatService = await self.get_group_service()
        await service.delete_group()

    async def disconnect(self, close_code):
        """Disconect to ws"""
        await self.channel_layer.group_discard(self.chat_group, self.channel_name)

    # Receive message from WebSocket
    async def receive_json(self, content: dict):
        message_type = content.get('message_type', None)
        if message_type == 'chat.message':
            await self.handle_message(content)
        elif message_type == 'chat.delete_message':
            await self.handle_delete_message(content)
        elif message_type == 'chat.edit_message':
            await self.handle_edit_message(content)
        elif message_type == 'chat.delete_user':
            await self.handle_delete_user(content)
        elif message_type == 'chat.leave_user':
            await self.handle_leave_user()
        elif message_type == 'chat.add_user':
            await self.handle_add_users(content)
        elif message_type == 'chat.delete_chat':
            await self.handle_delete_chat()
        else:
            logger.exception("Нет такого метода в ws!")
            raise ValueError("Нет такого метода в ws!")

    async def handle_message(self, content):
        new_message = await self.create_message(content['message'])
        await self.channel_layer.group_send(
            self.chat_group, {"type": "chat.message",
                              "message": new_message}
        )

    async def handle_delete_message(self, content):
        await self.delete_message(message_id=content.get("message_id"))
        await self.channel_layer.group_send(
            self.chat_group, {"type": "chat.delete_message",
                              "message": content.get("message_id")}
        )

    async def handle_edit_message(self, content):
        edited_message = await self.edit_message(content.get("message_id"),
                                                 content.get('message_text'),
                                                 content.get('chat'))
        await self.channel_layer.group_send(
            self.chat_group, {"type": "chat.edit_message",
                              "message": edited_message}
        )

    async def handle_delete_user(self, content):
        deleted_user, message = await self.delete_user(user=content.get("deleted_user"))
        await self.channel_layer.group_send(
            self.chat_group, {"type": "chat.delete_user",
                              "deleted_user": deleted_user}
        )

        await self.channel_layer.group_send(
            self.chat_group, {"type": "chat.message",
                              "message": message}
        )

    async def handle_leave_user(self):
        leaved_user, message = await self.leave_user()
        await self.channel_layer.group_send(
            self.chat_group, {"type": "chat.leave_user",
                              "leaved_user": leaved_user,
                              "message": message}
        )

        await self.channel_layer.group_send(
            self.chat_group, {"type": "chat.message",
                              "message": message}
        )

    async def handle_add_users(self, content):
        new_users, messages = await self.add_users(users=content.get('users'))
        await self.channel_layer.group_send(
            self.chat_group, {"type": "chat.add_users",
                              "new_users": new_users}
        )
        for message in messages:
            await self.channel_layer.group_send(
                self.chat_group, {"type": "chat.message",
                                  "message": message}
            )

    async def handle_delete_chat(self):
        await self.delete_chat()
        await self.channel_layer.group_send(
            self.chat_group, {"type": "chat.deleted_chat",}
        )

    async def chat_message(self, event):
        if self.scope['user'].pk != int(event['message']['user']['id']):
            await self.update_notifications()
        await self.send_json({"message": event['message']})

    async def chat_delete_message(self, event):
        await self.send_json({"deleted_message": event['message']})

    async def chat_edit_message(self, event):
        await self.send_json({"edited_message": event['message']})

    async def chat_delete_user(self, event):
        await self.send_json({"deleted_user": event['deleted_user']})

    async def chat_leave_user(self, event):
        await self.send_json({"leaved_user": event['leaved_user']})

    async def chat_add_users(self, event):
        await self.send_json({"new_users": event['new_users']})

    async def chat_deleted_chat(self, event):
        await self.send_json({"deleted_chat": True})

