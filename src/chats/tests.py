from io import BytesIO

from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from users.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import GroupSettings, Chat, GroupSettingsHasUser, Message, MessageContent

"""ВНИМАНИЕ !
Все тесты кроме CreateChatTest() не работает, так как API было заменено WS !
Нужно переписать тесты под WebsocketConsumer
"""


def create_users():
    user = CustomUser.objects.create_user(
        id=0,
        username='testuser',
        email='testuser@example.com',
        password='testpass123'
    )
    CustomUser.objects.create_user(
        id=1,
        username='test1',
        email='testuser@example.my',
        password='testpass123'
    )
    CustomUser.objects.create_user(
        id=2,
        username='test2',
        email='testuser123@example.my',
        password='testpass123'
    )
    client = APIClient()
    return user, client


class CreateChatTests(APITestCase):
    """Класс для тестирования создания новых чатов"""

    def setUp(self):
        self.user, self.client = create_users()
        self.client.force_authenticate(user=self.user)

    def test_private_chat(self):
        url = reverse('create-private')
        data = {'current_users': ['test1'],
                'chat_type': 'P',
                'host': 0}
        response = self.client.post(url, data, format='json')
        response2 = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_group_chat(self):
        url = reverse('create-group')
        data = {'current_users': ['test1', 'test2'],
                'chat_type': 'G',
                'host': 0,
                'title': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GroupUsersChangeTests(APITestCase):
    """тестируем функционал групповых чатов"""
    def setUp(self):
        self.user, self.client = create_users()
        self.client.force_authenticate(user=self.user)
        url = reverse('create-group')
        data = {'current_users': ['test1', 'test2'],
                'chat_type': 'G',
                'host': 0,
                'title': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.newUser = CustomUser.objects.create_user(
            id=3,
            username='test3',
            email='testuser1gg@example.my',
            password='testpass123'
        )
        self.chat = Chat.objects.last().pk

    def test_add_user(self):
        """Добавление пользователя"""
        url = reverse('group-chat-users', kwargs={'pk': self.chat})
        data = {'current_users': [self.newUser.username]}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('current_users')[-1], 'test3')
        try:
            GroupSettingsHasUser.objects.get(group_settings=GroupSettings.objects.last().pk, user=self.newUser)
        except ObjectDoesNotExist:
            self.fail("Настройки не создались !")

    def test_delete_user(self):
        """удаление пользователя"""
        url = reverse('group-chat-users', kwargs={'pk': self.chat})
        data = {'current_users': ['test2']}
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('current_users')[-1], 'test1')

        with self.assertRaises(ObjectDoesNotExist):
            GroupSettingsHasUser.objects.get(group_settings=1, user=CustomUser.objects.get(username='test2'))

    def test_delete_owner(self):
        """попытка удалить владельца"""
        url = reverse('group-chat-users', kwargs={'pk': self.chat})
        data = {'current_users': ['testuser']}
        with self.assertRaises(ValueError) as context_manager:
            response = self.client.delete(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('Вы не можете удалить владельца чата', str(context_manager.exception))

    def test_leave_to_room(self):
        """Пльзователь покидает группу"""
        self.client.force_authenticate(user=CustomUser.objects.get(username='test2'))
        url = reverse('group-chat-users', kwargs={'pk': self.chat})
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('current_users')[-1], 'test1')

    def test_delete_group(self):
        """удаляем группу"""
        self.client.force_authenticate(user=self.user)
        url = reverse('group-chat-detail', kwargs={'pk': self.chat})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Chat.objects.all()), 0)
        self.assertEqual(len(GroupSettingsHasUser.objects.all()), 0)
        self.assertEqual(len(GroupSettings.objects.all()), 0)


class GroupSettingsChange(APITestCase):
    """Тесты по изменению данных группы"""
    def setUp(self):
        self.user, self.client = create_users()
        self.client.force_authenticate(user=self.user)
        url = reverse('create-group')
        data = {'current_users': ['test1', 'test2'],
                'chat_type': 'G',
                'host': 0,
                'title': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.chat = Chat.objects.all()[0]
        self.group_settings = GroupSettings.objects.get(chat=self.chat)
        self.pk = self.group_settings.pk

        self.image_data = BytesIO()
        image = Image.new('RGB', (100, 100), "white")
        image.save(self.image_data, format='png')
        self.image_data.seek(0)

    def test_retrieve(self):
        """Отображение"""
        url = reverse('group-settings', kwargs={'pk': self.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_title(self):
        """Изменение названия"""
        url = reverse('group-settings', kwargs={'pk': self.pk})
        data = {'title': 'newTitle'}
        response = self.client.patch(url, data, format='json')
        obj = GroupSettings.objects.get(chat=self.chat, pk=self.pk)

        self.assertEqual(obj.title, "newTitle", "title not equal!")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_avatar(self):
        """Изменение аватара"""
        url = reverse('group-settings', kwargs={'pk': self.pk})
        data = {'avatar': SimpleUploadedFile('avatar.png', self.image_data.read(), content_type='image/png')}
        response = self.client.patch(url, data, format='multipart')
        obj = GroupSettings.objects.get(chat=self.chat, pk=self.pk)

        self.assertNotEqual(obj.avatar, "default.jpg", "avatar not equal!")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_group_data(self):
        """Изменение всех данных"""
        url = reverse('group-settings', kwargs={'pk': self.pk})
        data = {'avatar': SimpleUploadedFile('avatar.png', self.image_data.read(), content_type='image/png'),
                'title': 'newTitle'}
        response = self.client.patch(url, data, format='multipart')
        obj = GroupSettings.objects.get(chat=self.chat, pk=self.pk)

        self.assertNotEqual(obj.avatar, "default.jpg", "avatar not equal!")
        self.assertEqual(obj.title, "newTitle", "title not equal!")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GroupSettingsHasUserTests(APITestCase):
    """Тестируем смену ролей"""
    def setUp(self):
        self.user, self.client = create_users()
        self.client.force_authenticate(user=self.user)
        url = reverse('create-group')
        data = {'current_users': ['test1', 'test2'],
                'chat_type': 'G',
                'host': 0,
                'title': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.group_settings = GroupSettings.objects.last()
        self.other_user = CustomUser.objects.get(pk=1)

    def test_change_role_to_admin(self):
        """смена роли на админа"""
        url = reverse('group-settings-has-user')
        data = {'group_settings': self.group_settings.pk,
                "user": self.other_user.pk,
                "role": "A"}
        response = self.client.patch(url, data, format='json')
        obj = GroupSettingsHasUser.objects.get(user=self.other_user.pk)
        self.assertEqual(obj.get_role_display(), 'admin', "not equal roles")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_role_to_owner(self):
        """смена роли на владельца"""
        url = reverse('group-settings-has-user')
        data = {'group_settings': self.group_settings.pk,
                "user": self.user.pk,
                "role": "O"}
        response = self.client.patch(url, data, format='json')
        obj = GroupSettingsHasUser.objects.get(user=self.other_user.pk)
        self.assertNotEqual(obj.get_role_display(), 'owner', "not equal roles")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_role_to_default(self):
        """смена роли к обычной"""
        url = reverse('group-settings-has-user')
        data = {'group_settings': self.group_settings.pk,
                "user": self.user.pk,
                "role": "D"}
        response = self.client.patch(url, data, format='json')
        obj = GroupSettingsHasUser.objects.get(user=self.other_user.pk)
        self.assertEqual(obj.get_role_display(), 'default', "not equal roles")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_role_to_admin_error(self):
        """попытке присвоения роли админа без нужных прав"""
        self.client.force_authenticate(user=self.other_user)
        url = reverse('group-settings-has-user')
        data = {'group_settings': self.group_settings.pk,
                "user": self.other_user.pk,
                "role": "A"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MessageTests(APITestCase):

    def setUp(self):
        self.user, self.client = create_users()
        self.client.force_authenticate(user=self.user)
        url = reverse('create-group')
        data = {'current_users': ['test1', 'test2'],
                'chat_type': 'G',
                'host': 0,
                'title': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.obj = Chat.objects.last()
        content_type = MessageContent.objects.get_or_create(
                        name=MessageContent.TypeOfMessageContent.TEXT)
        self.message = Message.objects.create(chat=self.obj,
                                              user=self.user,
                                              content_type=content_type[0],
                                              text_content='testContent')

    def test_edit_message(self):
        url = reverse('message', kwargs={"pk": self.message.pk})
        data = {"text_content": "editContent",
                "chat": self.obj.pk}
        response = self.client.patch(url, data, format="json")
        obj = Message.objects.get(pk=self.message.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(obj.text_content, "editContent")

    def test_delete_message(self):
        url = reverse('message', kwargs={"pk": self.message.pk})
        data = {"chat": self.obj.pk}
        response = self.client.delete(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Message.objects.all()), 0)