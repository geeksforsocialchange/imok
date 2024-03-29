# Generated by Django 3.2.2 on 2021-05-10 17:16

import application.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0020_auto_20210509_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='telegram_username',
            field=models.CharField(blank=True, default='', help_text="Without the initial '@'", max_length=32, null=True, unique=True, validators=[application.models.validate_telegram_username]),
        ),
    ]
