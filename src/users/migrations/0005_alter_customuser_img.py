# Generated by Django 5.0.4 on 2024-06-07 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_customuser_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='img',
            field=models.ImageField(default='user_avatars/default.jpg', upload_to='user_avatar_upload_path', verbose_name='Аватар'),
        ),
    ]
