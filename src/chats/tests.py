from io import BytesIO

from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from users.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import GroupSettings, Chat, GroupSettingsHasUser


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


# class GroupUsersChangeTests(APITestCase):
#     """тестируем функционал групповых чатов"""
#     def setUp(self):
#         self.user, self.client = create_users()
#         self.client.force_authenticate(user=self.user)
#
#     def test_add_user(self):
#         pass
#
#     def test_delete_user(self):
#         pass
#
#     def test_change_role_user(self):
#         pass
#
#     def test_delete_group(self):
#         pass

class GroupSettingsChange(APITestCase):

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
        url = reverse('group-settings', kwargs={'pk': self.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_title(self):
        url = reverse('group-settings', kwargs={'pk': self.pk})
        data = {'title': 'newTitle'}
        response = self.client.patch(url, data, format='json')
        obj = GroupSettings.objects.get(chat=self.chat, pk=self.pk)

        self.assertEqual(obj.title, "newTitle", "title not equal!")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_avatar(self):
        url = reverse('group-settings', kwargs={'pk': self.pk})
        data = {'avatar': SimpleUploadedFile('avatar.png', self.image_data.read(), content_type='image/png')}
        response = self.client.patch(url, data, format='multipart')
        obj = GroupSettings.objects.get(chat=self.chat, pk=self.pk)

        self.assertNotEqual(obj.avatar, "default.jpg", "avatar not equal!")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_group_data(self):
        url = reverse('group-settings', kwargs={'pk': self.pk})
        data = {'avatar': SimpleUploadedFile('avatar.png', self.image_data.read(), content_type='image/png'),
                'title': 'newTitle'}
        response = self.client.patch(url, data, format='multipart')
        obj = GroupSettings.objects.get(chat=self.chat, pk=self.pk)

        self.assertNotEqual(obj.avatar, "default.jpg", "avatar not equal!")
        self.assertEqual(obj.title, "newTitle", "title not equal!")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GroupSettingsHasUserTests(APITestCase):
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
        url = reverse('group-settings-has-user')
        data = {'group_settings': self.group_settings.pk,
                "user": self.other_user.pk,
                "role": "A"}
        response = self.client.patch(url, data, format='json')
        obj = GroupSettingsHasUser.objects.get(user=self.other_user.pk)
        self.assertEqual(obj.get_role_display(), 'admin', "not equal roles")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_role_to_owner(self):
        url = reverse('group-settings-has-user')
        data = {'group_settings': self.group_settings.pk,
                "user": self.user.pk,
                "role": "O"}
        response = self.client.patch(url, data, format='json')
        obj = GroupSettingsHasUser.objects.get(user=self.other_user.pk)
        self.assertNotEqual(obj.get_role_display(), 'owner', "not equal roles")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_role_to_default(self):
        url = reverse('group-settings-has-user')
        data = {'group_settings': self.group_settings.pk,
                "user": self.user.pk,
                "role": "D"}
        response = self.client.patch(url, data, format='json')
        obj = GroupSettingsHasUser.objects.get(user=self.other_user.pk)
        self.assertEqual(obj.get_role_display(), 'default', "not equal roles")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_role_to_admin_error(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse('group-settings-has-user')
        data = {'group_settings': self.group_settings.pk,
                "user": self.other_user.pk,
                "role": "A"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
