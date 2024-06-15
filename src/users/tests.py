from django.urls import reverse
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import CustomUser


def create_user():
    user = CustomUser.objects.create_user(
        id=0,
        username='testuser',
        email='testuser@example.com',
        password='testpass123'
    )
    return user


class ChangeProfileDataTest(APITestCase):

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.image_data = BytesIO()
        image = Image.new(mode="RGB", size=(100, 100), color="white")
        image.save(self.image_data, format='png')
        self.image_data.seek(0)

        self.image = SimpleUploadedFile(name='test.png', content=self.image_data.read(), content_type='image/png')

    def tests_change_status(self):
        url = reverse('profile', kwargs={"user_id": self.user.pk})
        data = {"status": "newStatus"}
        response = self.client.patch(url, data, format='json')

        obj = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(obj.status, "newStatus")

    def tests_change_name(self):
        url = reverse('profile', kwargs={"user_id": self.user.pk})
        data = {"name": "testName"}
        response = self.client.patch(url, data, format='json')

        obj = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(obj.name, "testName")

    def tests_change_avatar(self):
        url = reverse('profile', kwargs={"user_id": self.user.pk})
        data = {"img": self.image}
        response = self.client.patch(url, data, format='multipart')

        obj = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(obj.img, "default.jpg")

    def tests_change_all(self):
        url = reverse('profile', kwargs={"user_id": self.user.pk})
        data = {
            "status": 'newStatus',
            "name": "testName",
            "img": self.image}
        response = self.client.patch(url, data, format='multipart')

        obj = CustomUser.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(obj.status, "newStatus")
        self.assertEqual(obj.name, "testName")
        self.assertNotEqual(obj.img, "default.jpg")

