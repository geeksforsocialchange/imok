from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Subscriber(models.Model):
    phone_number = PhoneNumberField(max_length=20, unique=True, primary_key=True)
    name = models.TextField()


class Checkin(models.Model):
    phone_number = models.OneToOneField(Subscriber, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)


class Invite(models.Model):
    phone_number = PhoneNumberField(max_length=20, unique=True, primary_key=True)
