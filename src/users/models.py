import os.path

from django.core.cache import cache
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


def user_avatar_upload_path(instance, filename):

    ext = filename.split('.')[-1]
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    new_filename = f"{timestamp}.{ext}"
    folder = f'user_avatars/user_{instance.id}'
    path = os.path.join(settings.MEDIA_ROOT, folder)
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    return os.path.join(folder, new_filename)


class CustomUser(AbstractUser):
    name = models.CharField(max_length=50, verbose_name='Имя пользователя')
    status = models.CharField(verbose_name='Статус')
    img = models.ImageField(upload_to=user_avatar_upload_path, verbose_name='Аватар',
                            default='user_avatars/default.jpg')

    def is_online(self):
        last_seen = cache.get(f"last-seen-{self.pk}")
        if last_seen is not None and timezone.now() < last_seen + timezone.timedelta(seconds=300):
            return True
        return False

    def __str__(self):
        return f"Name: {self.name}, Status: {self.status}"




