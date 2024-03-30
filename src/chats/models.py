from django.db import models
from django.conf import settings


class Chat(models.Model):
    class TypesOfChats(models.TextChoices):
        PRIVATE = 'P', 'private'
        GROUP = 'G', 'group'

    chat_type = models.CharField(max_length=1, choices=TypesOfChats)
    chat_content = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='Message', related_name='chat')

    objects = models.Manager()

    def __str__(self):
        return f"Type: {self.chat_type}, "


class MessageContent(models.Model):
    class TypeOfMessageContent(models.TextChoices):
        AUDIO = 'A', 'audio'
        VIDEO = 'V', 'video'
        TEXT = 'T', 'text'
        IMG = 'I', 'image'
        FILE = 'F', 'file'

    name = models.CharField(max_length=5, choices=TypeOfMessageContent)

    objects = models.Manager()

    def __str__(self):
        return f"{self.name}"


class Message(models.Model):
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    content_type = models.ForeignKey(to=MessageContent, on_delete=models.PROTECT)
    reply = models.BooleanField(default=False)
    text_content = models.TextField()
    audio_content = models.FileField()
    video_content = models.FileField()
    file_content = models.FileField()
    img_content = models.ImageField()

    objects = models.Manager()

    def __str__(self):
        return f"Chat: {self.chat}, User: {self.user}, Content_type: {self.content_type}"


class GroupSettings(models.Model):
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE)
    avatar = models.ImageField()
    title = models.CharField(max_length=255)
    user = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='GroupSettingsHasUser')

    objects = models.Manager()

    def __str__(self):
        return f"Chat: {self.chat}, Title: {self.title}, User: {self.user}"


class GroupSettingsHasUser(models.Model):

    class Role(models.TextChoices):
        ADMIN = 'A', 'admin'
        OWNER = 'O', 'owner'
        DEFAULT = 'D', 'default'

    group_settings = models.ForeignKey(to=GroupSettings, on_delete=models.CASCADE)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=7, choices=Role)

    objects = models.Manager()

    def __str__(self):
        return f"User: {self.user} Role: {self.role} Group_chat: {self.group_settings}"





















































































