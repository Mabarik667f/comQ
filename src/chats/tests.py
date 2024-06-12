from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from users.models import CustomUser


class CreateChatTests(APITestCase):
    """Класс для тестирования создания новых чатов"""

    def setUp(self):
        self.user = CustomUser.objects.create_user(
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
        self.client = APIClient()
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