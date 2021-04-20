# Generated by Django 3.2 on 2021-04-20 11:23

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0015_auto_20210418_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter a valid phone number (e.g. 0121 234 5678) or a number with an international call prefix.', max_length=20, null=True, region=None, unique=True),
        ),
        migrations.AlterField(
            model_name='metrichour',
            name='num',
            field=models.IntegerField(default=0, verbose_name='count'),
        ),
    ]
