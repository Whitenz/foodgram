# Generated by Django 3.2.15 on 2022-09-18 15:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220918_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='following',
            field=models.ManyToManyField(related_name='followers', through='users.Subscription', to=settings.AUTH_USER_MODEL),
        ),
    ]
