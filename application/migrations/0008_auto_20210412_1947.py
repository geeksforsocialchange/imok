# Generated by Django 3.1.7 on 2021-04-12 19:47

import application.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_member_telegram_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='telegram_chat_id',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='member',
            name='telegram_username',
            field=models.TextField(default='', validators=[application.models.validate_telegram_username]),
        ),
    ]
