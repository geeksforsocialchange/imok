# Generated by Django 3.1.6 on 2021-02-02 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='notes',
            field=models.TextField(default=''),
        ),
    ]
