from django.contrib.auth.models import AbstractUser
from django.db import models

from chats.models import Chat


def user_avatar_upload_path(instance, filename):
    pass


class CustomUser(AbstractUser):
    name = models.CharField(max_length=50, verbose_name='Имя пользователя')
    status = models.CharField(verbose_name='Статус')
    img = models.ImageField(upload_to='user_avatar_upload_path', verbose_name='Аватар', blank=True)

    def __str__(self):
        return f"Name: {self.name}, Status: {self.status}"


class UserSettings(models.Model):
    param = models.CharField(max_length=10)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}"





