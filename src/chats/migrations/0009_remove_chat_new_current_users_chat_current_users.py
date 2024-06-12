# Generated by Django 5.0.4 on 2024-06-12 09:57

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0008_remove_chat_current_users'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='new_current_users',
        ),
        migrations.AddField(
            model_name='chat',
            name='current_users',
            field=models.ManyToManyField(blank=True, related_name='current_chats', through='chats.UserToChat', to=settings.AUTH_USER_MODEL),
        ),
    ]
