from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
import uuid

LANGUAGES = [('en_gb', 'English')]
SIGNING_CENTERS = [('dallas court', 'Dallas Court')]


class Member(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.TextField(default='')
    notes = models.TextField(default='', blank=True)
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=5, choices=LANGUAGES, default='en_gb')
    registered = models.BooleanField(default=False)
    phone_number = PhoneNumberField(max_length=20, unique=True, null=True)
    signing_center = models.CharField(choices=SIGNING_CENTERS, default='dallas court', max_length=50)


class Checkin(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
