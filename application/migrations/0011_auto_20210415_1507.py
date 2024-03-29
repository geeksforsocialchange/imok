# Generated by Django 3.2 on 2021-04-15 14:07

import application.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0010_auto_20210415_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='member',
            name='telegram_username',
            field=models.CharField(blank=True, default='', max_length=50, validators=[application.models.validate_telegram_username]),
        ),
    ]
