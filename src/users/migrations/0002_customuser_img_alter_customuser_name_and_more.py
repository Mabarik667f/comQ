# Generated by Django 5.0.3 on 2024-03-13 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='img',
            field=models.ImageField(blank=True, upload_to='img/', verbose_name='Аватар'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Имя пользователя'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='status',
            field=models.CharField(verbose_name='Статус'),
        ),
    ]
