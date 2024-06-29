from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from django.core.cache import cache
from rest_framework.generics import get_object_or_404

from users.models import CustomUser

from .models import Chat, Message, MessageContent, UserToChat, GroupSettings
from .serializers import ChatSerializer, MessageSerializer, GroupSettingsSerializer
from users.serializers import UserProfileSerializer, UserDataOnChatSerializer
import logging

from .services import GroupChatService
from django.utils import timezone

logger = logging.getLogger("consumer")


class ConsumersMethods:

    def __init__(self, user):
        self.user = user

    @database_sync_to_async
    def get_serialized_data(self, serializer, pk, *args, **kwargs):
        return serializer(pk, *args, **kwargs).data

    @database_sync_to_async
    def get_chat(self, chat_pk):
        return Chat.objects.get(pk=chat_pk)

    @database_sync_to_async
    def save_group_channel_name(self, channel_name, chat_id):
        cache.set(f"channel_{chat_id}", channel_name, timeout=None)

    @database_sync_to_async
    def get_group_channel_name(self, chat_id):
        return cache.get(f"channel_{chat_id}")

    @database_sync_to_async
    def delete_group_channel_name(self, chat_id):
        cache.delete(f"channel_{chat_id}")

    async def get_serialized_chat_data(self, chat_pk):
        chat_data = await self.get_chat(chat_pk)
        return await self.get_serialized_data(ChatSerializer, chat_data)

    @database_sync_to_async
    def update_notifications(self, chat_pk, delete=False):
        user_to_chat = UserToChat.objects.filter(chat_id=chat_pk, user_id=self.user)
        if user_to_chat.exists():
            user_to_chat = user_to_chat[0]
            if not delete:
                user_to_chat.count_notifications = user_to_chat.count_notifications + 1
            else:
                user_to_chat.count_notifications = user_to_chat.count_notifications - 1
            user_to_chat.save()

    async def get_group_service(self, chat_pk):
        chat: Chat = await self.get_chat(chat_pk)
        return GroupChatService(user=self.user, chat=chat)

    async def create_message(self, message, chat, system=False, reply=False):
        chat: Chat = await self.get_chat(chat)
        content_type = await database_sync_to_async(MessageContent.objects.get_or_create)(
            name=MessageContent.TypeOfMessageContent.TEXT
        )
        new_message = await database_sync_to_async(Message.objects.create)(
            chat=chat,
            user=self.user,
            content_type=content_type[0],
            text_content=message,
            system=system,
            reply=reply
        )

        return await self.get_serialized_data(MessageSerializer, new_message)


class HubConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.hub = f"hub"
        self.methods = ConsumersMethods(user=self.scope['user'])

        await self.channel_layer.group_add(self.hub, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Disconect to ws"""
        await self.channel_layer.group_discard(self.hub, self.channel_name)

    async def receive_json(self, content: dict):
        message_type = content.get('message_type', None)
        if message_type == 'chat.delete_user':
            await self.handle_delete_user(content)
        elif message_type == 'chat.leave_user':
            await self.handle_leave_user(content)
        elif message_type == 'chat.add_user':
            await self.handle_add_users(content)
        else:
            logger.exception("Нет такого метода в ws!")
            raise ValueError("Нет такого метода в ws!")

    async def handle_delete_user(self, content):
        deleted_user, message = await self.delete_user(user=content.get("deleted_user"),
                                                       chat_pk=content.get('chat_pk'))

        chat = await self.methods.get_serialized_chat_data(chat_pk=content.get('chat_pk'))
        await self.channel_layer.group_send(
            self.hub, {"type": "chat.delete_user",
                       "deleted_user": deleted_user,
                       "chat": chat}
        )

        await self.force_user_disconnect(chat_pk=content.get('chat_pk'),
                                         user_pk=deleted_user['id'],
                                         method="delete")

        await self.send_message(message, chat_pk=content.get('chat_pk'), chat=chat)

    async def handle_leave_user(self, content):

        leaved_user, message = await self.leave_user(chat_pk=content.get('chat_pk'))
        chat = await self.methods.get_serialized_chat_data(chat_pk=content.get('chat_pk'))

        await self.channel_layer.group_send(
            self.hub, {"type": "chat.leave_user",
                       "leaved_user": leaved_user,
                       "chat": chat}
        )

        await self.force_user_disconnect(chat_pk=content.get('chat_pk'),
                                         user_pk=self.scope['user'].pk,
                                         method="leave")

        await self.send_message(message, chat_pk=content.get('chat_pk'), chat=chat)

    async def handle_add_users(self, content):
        new_users, messages = await self.add_users(users=content.get('users'),
                                                   chat_pk=content.get('chat_pk'))
        chat = await self.methods.get_serialized_chat_data(chat_pk=content.get('chat_pk'))
        await self.channel_layer.group_send(
            self.hub, {"type": "chat.add_users",
                       "new_users": new_users,
                       "chat": chat}
        )
        for message in messages:
            await self.send_message(message, chat_pk=content.get('chat_pk'), chat=chat)

    async def send_message(self, message, chat_pk, chat, **kwargs):
        channel_group = f"chat_{chat_pk}"
        event = {"type": "chat.message",
                 "message": message,
                 "chat_pk": chat_pk,
                 "chat": chat,
                 **kwargs}
        await self.channel_layer.group_send(
            channel_group, event
        )

    async def chat_delete_user(self, event):
        await self.send_json({"deleted_user": event['deleted_user'], "chat": event['chat']})

    async def chat_leave_user(self, event):
        await self.send_json({"leaved_user": event['leaved_user'], "chat": event['chat']})

    async def chat_add_users(self, event):
        await self.send_json({"new_users": event['new_users'], "chat": event['chat']})

    async def chat_message(self, event):
        if self.scope['user'].pk != int(event['message']['user']['id']):
            await self.methods.update_notifications(chat_pk=event['chat_pk'])
        await self.send_json({"message": event['message'], "chat": event['chat']})

    async def force_user_disconnect(self, chat_pk, user_pk, method):
        if self.scope['user'].pk == user_pk and method == 'leave':
            channel_name = await self.methods.get_group_channel_name(chat_id=chat_pk)

            await self.channel_layer.send(
                channel_name, {"type": "force.disconnect",
                               "user_pk": user_pk,
                               "method": 'leave'}
            )
        elif method == 'delete':
            channel_group = f"chat_{chat_pk}"

            await self.channel_layer.group_send(
                channel_group, {"type": "force.disconnect",
                                "user_pk": user_pk,
                                "method": 'delete'}
            )

    async def delete_user(self, user, chat_pk):
        user: CustomUser = await database_sync_to_async(CustomUser.objects.get)(username=user)
        service: GroupChatService = await self.methods.get_group_service(chat_pk)
        await service.delete_user(deleted_user=user)
        serializer_data = await self.methods.get_serialized_data(UserDataOnChatSerializer, user)
        message = await self.methods.create_message(f"Пользователь {serializer_data['name']} был удален!",
                                                    chat=chat_pk, system=True)
        return serializer_data, message

    async def leave_user(self, chat_pk):
        service: GroupChatService = await self.methods.get_group_service(chat_pk)
        await service.leave_user()
        serializer_data = await self.methods.get_serialized_data(UserDataOnChatSerializer, self.scope['user'])
        message = await self.methods.create_message(f"Пользователь {serializer_data['name']} покинул чат!",
                                                    chat=chat_pk, system=True)
        return serializer_data, message

    async def add_users(self, users, chat_pk):
        new_users = []
        messages = []
        chat: Chat = await self.methods.get_chat(chat_pk=chat_pk)
        service: GroupChatService = await self.methods.get_group_service(chat_pk)
        for user in users:
            user = user.get('value')
            user: CustomUser = await database_sync_to_async(CustomUser.objects.get)(username=user)
            await service.add_user(added_user=[user])
            await database_sync_to_async(user.refresh_from_db)()
            user_data = await self.methods.get_serialized_data(UserDataOnChatSerializer, user,
                                                               context={"chat": chat})
            new_users.append(user_data)
            message = await self.methods.create_message(f"Пользователь {user_data['name']} был добавлен!",
                                                        system=True, chat=chat_pk)
            messages.append(message)
        return new_users, messages


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """Connect to ws"""
        self.chat_pk = self.scope["url_route"]["kwargs"]["chat"]
        self.chat_group = f"chat_{self.chat_pk}"
        self.methods = ConsumersMethods(user=self.scope['user'])

        await self.channel_layer.group_add(self.chat_group, self.channel_name)
        await self.methods.save_group_channel_name(self.channel_name, self.chat_pk)

        chat: Chat = await self.methods.get_chat(self.chat_pk)
        data = await self.methods.get_serialized_data(ChatSerializer, chat)

        await self.accept()
        await self.send_json(content=data)

    @database_sync_to_async
    def current_users(self):
        chat = Chat.objects.get(pk=self.chat_pk)
        return [UserProfileSerializer(user).data for user in chat.current_users.all()]

    @database_sync_to_async
    def get_group_settings(self):
        return get_object_or_404(GroupSettings, chat=Chat.objects.get(pk=self.chat_pk))

    async def delete_message(self, message_id):
        message = await database_sync_to_async(Message.objects.get)(pk=message_id)
        await database_sync_to_async(message.delete)()
        return await self.methods.get_serialized_data(MessageSerializer, message)

    async def edit_message(self, message_id, message_text, chat):
        message = await database_sync_to_async(Message.objects.get)(pk=message_id)
        serializer = await database_sync_to_async(MessageSerializer)(data={"text_content": message_text, "chat": chat})
        await database_sync_to_async(serializer.is_valid)(raise_exception=True)
        await database_sync_to_async(serializer.update)(instance=message, validated_data=serializer.validated_data)
        return await self.methods.get_serialized_data(MessageSerializer, message)

    async def delete_chat(self):
        service: GroupChatService = await self.methods.get_group_service(self.chat_pk)
        await service.delete_group()

    @database_sync_to_async
    def clear_notifications(self):
        user_to_chat = UserToChat.objects.filter(chat_id=self.chat_pk, user_id=self.scope['user'].pk)
        if user_to_chat.exists():
            user_to_chat = user_to_chat[0]
            user_to_chat.count_notifications = 0
            user_to_chat.save()

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
        elif message_type == 'chat.delete_chat':
            await self.handle_delete_chat()
        elif message_type == 'chat.clear_notifications':
            await self.handle_clear_notifications()
        else:
            logger.exception("Нет такого метода в ws!")
            raise ValueError("Нет такого метода в ws!")

    async def handle_message(self, content):
        new_message = await self.methods.create_message(content['message'], reply=content['reply'],
                                                        chat=self.chat_pk)
        await self.channel_layer.group_send(
            self.chat_group, {"type": "chat.message",
                              "message": new_message}
        )

    async def handle_delete_message(self, content):
        deleted_message = await self.delete_message(message_id=content.get("message_id"))
        delete_author = await self.methods.get_serialized_data(UserDataOnChatSerializer, self.scope['user'])
        await self.channel_layer.group_send(
            self.chat_group, {"type": "chat.delete_message",
                              "message": deleted_message,
                              "delete_author": delete_author}
        )

    async def handle_edit_message(self, content):
        edited_message = await self.edit_message(content.get("message_id"),
                                                 content.get('message_text'),
                                                 content.get('chat'))
        await self.channel_layer.group_send(
            self.chat_group, {"type": "chat.edit_message",
                              "message": edited_message}
        )

    async def handle_delete_chat(self):
        await self.delete_chat()
        await self.channel_layer.group_send(
            self.chat_group, {"type": "chat.deleted_chat", }
        )

    async def handle_clear_notifications(self):
        await self.clear_notifications()

        await self.channel_layer.send(
            self.channel_name, {"type": "chat.clear_notifications"}
        )

    async def chat_message(self, event):
        if self.scope['user'].pk != int(event['message']['user']['id']):
            await self.methods.update_notifications(chat_pk=self.chat_pk)
        await self.send_json({"message": event['message']})

    async def chat_delete_message(self, event):
        if self.scope['user'].pk != int(event['message']['user']['id'])\
                and self.scope['user'].pk != int(event['delete_author']['id']):
            await self.methods.update_notifications(chat_pk=self.chat_pk, delete=True)
        await self.send_json({"deleted_message": event['message'],
                              "delete_author": event['delete_author']})

    async def chat_edit_message(self, event):
        await self.send_json({"edited_message": event['message']})

    async def chat_deleted_chat(self, event):
        await self.send_json({"deleted_chat": True})

    async def chat_clear_notifications(self, event):
        await self.send_json({"clear_notifications": True})

    async def force_disconnect(self, event):
        if event['method'] == 'leave':
            await self.force_disconnect_accept()
        elif event['method'] == 'delete' and self.scope['user'].pk == event['user_pk']:
            await self.force_disconnect_accept()

    async def force_disconnect_accept(self):
        await self.methods.delete_group_channel_name(chat_id=self.chat_pk)
        await self.close(code=1000)
