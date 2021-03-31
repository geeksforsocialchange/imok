from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
import uuid
from twilio.rest import Client
from django.utils import timezone
from imok.settings import CHECKIN_TTL, NOTIFY_EMAIL, TWILIO_AUTH_TOKEN, TWILIO_ACCOUNT_SID, TWILIO_FROM_NUMBER
from django.utils.translation import gettext as _

from django.core.mail import send_mail

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
    is_ok = models.BooleanField(null=True)
    is_warning = models.BooleanField(null=False, default=False)

    def ok_status(self):
        state = {
            None: _("Maybe ok"),
            True: _("OK"),
            False: _("Not OK")
        }
        return state[self.is_ok]

    def sign_in(self):
        in_time = timezone.now()
        out_time = in_time + CHECKIN_TTL

        self.is_ok = True
        self.is_warning = False
        self.save()
        checkin, created = Checkin.objects.update_or_create(member=self, defaults={'time_stamp': in_time})
        if created:
            response = " ".join([
                _("You were checked in at %(center)s at %(time)s") % {'center': self.signing_center,
                                                                      'time': str(in_time.time())},
                _("We will alert our team if we don’t hear from you by %(time)s") % {'time': out_time}
            ])
        else:
            response = _("You were already checked in. Your check in time has been updated")
        return response

    def sign_out(self):
        self.is_ok = None
        self.is_warning = False
        self.save()

        try:
            checkin = Checkin.objects.get(member=self)
        except Checkin.DoesNotExist:
            return _("You were not checked in. To check in message IN")
        checkin.delete()
        return _("You were checked out at %(center)s at %(time)s") % {'center': self.signing_center,
                                                                      'time': str(timezone.now().time())}

    def handle_sos(self):
        # Expression cannot be simplified as this is actually Optional[boolean]
        if self.is_ok == False:
            return

        # Flag the member as not ok
        self.is_ok = False
        self.save()

        # send an email
        subject = f"[IMOK] {self.name} sent an SOS"
        body = f"{self.name} sent an SOS from {self.signing_center}.  Here are their notes:\n\n{self.notes}."
        send_mail(subject,
                  body,
                  from_email="noreply@imok.wheresalice.info",  # @TODO make this configurable
                  recipient_list=[NOTIFY_EMAIL]  # @TODO make this configurable
                  )
        return _("Thanks for letting us know, our staff have been notified")


class Checkin(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def warn(self):
        # Only send a warning if we haven't already done so:
        if not self.member.is_warning:
            self.member.is_warning = True
            self.member.save()

            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=_("Are you OK? The alarm is about to be raised. Text OUT if you’re OK."),
                from_=TWILIO_FROM_NUMBER,
                to=self.member.phone_number.as_e164
            )
            print(message.sid)


    def timeout(self):
        # Have we already handled this timeout?
        # Your IDE may say we can simplify this, but we can't
        if self.member.is_ok == False:
            return

        self.member.is_ok = False
        self.member.is_warning = False
        self.member.save()

        subject = f"[IMOK] {self.member.name} is not ok"
        body = f"{self.member.name} failed to sign out at {self.member.signing_center}. They signed in at {self.time_stamp}. Here are their notes:\n\n{self.member.notes}."
        send_mail(subject,
                  body,
                  from_email="noreply@imok.wheresalice.info",  # @TODO make this configurable
                  recipient_list=[NOTIFY_EMAIL]  # @TODO make this configurable
                  )

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=_("You have failed to sign out, the admins have been notified"),
            from_=TWILIO_FROM_NUMBER,
            to=self.member.phone_number.as_e164
        )
        print(message.sid)

