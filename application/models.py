from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from twilio.rest import Client
from imok.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER


class Subscriber(models.Model):
    phone_number = PhoneNumberField(max_length=20, unique=True, primary_key=True)
    name = models.TextField()
    notes = models.TextField(default='')


class Checkin(models.Model):
    phone_number = models.OneToOneField(Subscriber, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)


class Invite(models.Model):
    phone_number = PhoneNumberField(max_length=20, unique=True, primary_key=True)

    def save(self, *args, **kwargs):
        print(f"Sending an invite to {self.phone_number.as_e164}")
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            to=self.phone_number.as_e164,
            from_=TWILIO_FROM_NUMBER,
            body="You have been invited to use IMOK. Please reply with 'name' and then your name, for example "
                 "'name bob jones'."
        )
        print(message.sid)
        super(Invite, self).save(*args, **kwargs)
