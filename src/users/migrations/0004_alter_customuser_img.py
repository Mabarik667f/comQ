# Generated by Django 5.0.4 on 2024-06-05 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_usersettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='img',
            field=models.ImageField(blank=True, upload_to='user_avatar_upload_path', verbose_name='Аватар'),
        ),
    ]