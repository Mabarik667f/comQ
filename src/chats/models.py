from django.db import models
from django.conf import settings


class Chat(models.Model):
    class TypesOfChats(models.TextChoices):
        PRIVATE = 'P', 'private'
        GROUP = 'G', 'group'

    chat_type = models.CharField(max_length=1, choices=TypesOfChats)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chats')
    current_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='current_chats', blank=True)

    objects = models.Manager()

    def __str__(self):
        return f"Type: {self.chat_type}, {self.host}"


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
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='messages')
    content_type = models.ForeignKey(to=MessageContent, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
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
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE, related_name="group_settings")
    avatar = models.ImageField()
    title = models.CharField(max_length=255, blank=False, unique=True, null=False)
    user = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='GroupSettingsHasUser',
                                  related_name="group_settings")

    objects = models.Manager()

    def __str__(self):
        return f"Chat: {self.chat}, Title: {self.title}, User: {self.user}"


class GroupSettingsHasUser(models.Model):

    class Role(models.TextChoices):
        ADMIN = 'A', 'admin'
        OWNER = 'O', 'owner'
        DEFAULT = 'D', 'default'

    group_settings = models.ForeignKey(to=GroupSettings, on_delete=models.CASCADE,
                                       related_name="user_settings_in_group")
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="user_settings_in_group")
    role = models.CharField(max_length=7, choices=Role)

    objects = models.Manager()

    def __str__(self):
        return f"User: {self.user} Role: {self.role} Group_chat: {self.group_settings}"





















































































