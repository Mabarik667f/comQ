# Generated by Django 5.0.4 on 2024-06-18 21:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0009_remove_chat_new_current_users_chat_current_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupsettings',
            name='chat',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='group_settings', to='chats.chat'),
        ),
    ]