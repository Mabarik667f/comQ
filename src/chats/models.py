import os.path

from django.db import models, transaction
from django.conf import settings
from django.utils import timezone


def group_avatar_upload_path(instance, filename):
    ext = filename.split('.')[-1]

    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    new_filename = f"{timestamp}.{ext}"
    folder = f'chat_avatars/chat_{instance.id}'
    path = os.path.join(settings.MEDIA_ROOT, folder)
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)

    return os.path.join(folder, new_filename)


def message_file_content_upload_path(instance, filename):
    pass


class Chat(models.Model):
    class TypesOfChats(models.TextChoices):
        PRIVATE = 'P', 'private'
        GROUP = 'G', 'group'

    chat_type = models.CharField(max_length=1, choices=TypesOfChats)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chats')
    current_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UserToChat',
                                           related_name='current_chats', blank=True)

    objects = models.Manager()

    def __str__(self):
        return f"Type: {self.chat_type}, {self.host}"

    @transaction.atomic
    def add_users(self, users, group_settings=None):
        if self.chat_type == self.TypesOfChats.PRIVATE and isinstance(users, int):
            user = users
            self.current_users.add(user)
        elif self.chat_type == self.TypesOfChats.GROUP and group_settings:
            for user in users:
                self.current_users.add(user)
                if user == self.host:
                    group_settings.add_user_to_group(user, role='O')
                else:
                    group_settings.add_user_to_group(user)
        else:
            raise ValueError('error add user in current_users')

    @transaction.atomic
    def delete_user(self, user):
        if self.chat_type == 'G':
            del_user = UserToChat.objects.get(user=user, chat=self)
            del_user.delete()
            group_settings: GroupSettings = GroupSettings.objects.get(chat=self)
            group_settings.delete_user_from_group(user)
        else:
            raise ValueError('private chat not support this method!')


class UserToChat(models.Model):

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_to_chat')
    chat = models.ForeignKey(to=Chat, on_delete=models.CASCADE, related_name='user_to_chat')
    count_notifications = models.IntegerField(default=0)

    objects = models.Manager()

    def clear_notifications(self):
        """Пользователь открыл чат - уведомления пропали"""
        self.count_notifications = 0


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
    reply = models.ForeignKey(to='self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    system = models.BooleanField(default=False)

    text_content = models.TextField()
    audio_content = models.FileField(upload_to=message_file_content_upload_path)
    video_content = models.FileField(upload_to=message_file_content_upload_path)
    file_content = models.FileField(upload_to=message_file_content_upload_path)
    img_content = models.ImageField(upload_to=message_file_content_upload_path)

    objects = models.Manager()

    def __str__(self):
        return f"Chat: {self.chat}, User: {self.user}, Content_type: {self.content_type}"


class GroupSettings(models.Model):
    chat = models.OneToOneField(to=Chat, on_delete=models.CASCADE, related_name="group_settings")
    avatar = models.ImageField(upload_to=group_avatar_upload_path, default='chat_avatars/default.jpg')
    title = models.CharField(max_length=255, blank=False, null=False)
    users = models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='GroupSettingsHasUser',
                                  related_name="group_settings")

    objects = models.Manager()

    def __str__(self):
        return f"Chat: {self.chat}, Title: {self.title}, Users: {self.users.all()}"

    @transaction.atomic
    def add_user_to_group(self, user, role='D'):
        if not GroupSettingsHasUser.objects.filter(group_settings=self, user=user).exists():
            GroupSettingsHasUser.objects.create(group_settings=self, user=user, role=role)
        else:
            raise ValueError('Пользователь уже есть в группе')

    @transaction.atomic
    def delete_user_from_group(self, user):

        try:
            group_settings_has_user = GroupSettingsHasUser.objects.get(group_settings=self, user=user)
        except GroupSettingsHasUser.DoesNotExist:
            raise ValueError('Пользователь не состоит в группе')

        group_settings_has_user.delete()


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

    def change_role(self, admin, role):
        admin_obj = GroupSettingsHasUser.objects.get(user=admin,
                                                     group_settings=self.group_settings)

        if admin_obj.role in (self.Role.ADMIN, self.Role.OWNER):
            if role == self.Role.OWNER:
                raise ValueError('нельзя присвоить роль создателя')
            else:
                self.role = role
        else:
            raise ValueError('вы не являетесь админом!')





















































































