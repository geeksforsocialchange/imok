# Generated by Django 3.1.6 on 2021-03-07 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_auto_20210207_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_ok',
            field=models.BooleanField(null=True),
        ),
    ]
