# Generated by Django 3.2 on 2021-04-18 09:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0013_member_codename'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetricHour',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('metric', models.CharField(db_index=True, max_length=60, unique=True)),
                ('value', models.CharField(max_length=50)),
                ('num', models.IntegerField(default=0)),
                ('date', models.DateField()),
                ('hour', models.IntegerField(default=-1)),
            ],
        ),
    ]
