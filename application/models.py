from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils import translation
from django.core.exceptions import ValidationError

from .telegram_group import TelegramGroup
from .twilio import twilio_send
from .telegram import telegram_send
from .contact_admins import notify_admins

LANGUAGES = [('en_gb', 'English'), ('cy_GB', 'Welsh')]
SIGNING_CENTERS = [('dallas court', 'Dallas Court')]


def validate_telegram_username(value):
    if value.startswith("@"):
        raise ValidationError(
            _('%(value)s should not include the "@"'),
            params={'value': value},
        )


class Member(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    name = models.CharField(default='', max_length=50)
    notes = models.TextField(default='', blank=True)
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=5, choices=LANGUAGES, default='en_gb')
    registered = models.BooleanField(default=False)
    phone_number = PhoneNumberField(max_length=20, unique=True, null=True, blank=True)
    signing_center = models.CharField(choices=SIGNING_CENTERS, default='dallas court', max_length=50)
    is_ok = models.BooleanField(null=True)
    is_warning = models.BooleanField(null=False, default=False)
    telegram_username = models.CharField(default='', validators=[validate_telegram_username], blank=True, max_length=50)
    telegram_chat_id = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name


    def ok_status(self):
        state = {
            None: _("Maybe ok"),
            True: _("OK"),
            False: _("Not OK")
        }
        return state[self.is_ok]

    def sign_in(self):
        in_time = timezone.localtime()
        out_time = in_time + settings.CHECKIN_TTL

        self.is_ok = True
        self.is_warning = False
        self.save()
        checkin, created = Checkin.objects.update_or_create(member=self, defaults={'time_stamp': in_time})
        if created:
            response = " ".join([
                _("You were checked in at %(center)s at %(time)s") % {'center': self.signing_center,
                                                                      'time': str(in_time.time().strftime('%X'))},
                _("We will alert our team if we don’t hear from you by %(time)s") % {'time': out_time.strftime('%X')}
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
                                                                      'time': str(timezone.localtime().time().strftime('%H:%M:%S'))}

    def handle_sos(self):
        # Expression cannot be simplified as this is actually Optional[boolean]
        if self.is_ok == False:
            return

        # Flag the member as not ok
        self.is_ok = False
        self.save()

        # send notifications
        subject = f"[IMOK] {self.name} sent an SOS"
        body = f"{self.name} sent an SOS from {self.signing_center}.  Here are their notes:\n\n{self.notes}."
        notify_admins(subject, body)
        return _("Thanks for letting us know, our staff have been notified")

    def send_message(self, message):
        if self.telegram_chat_id != 0:
            telegram_send(self.telegram_chat_id, message)
        elif self.phone_number:
            twilio_send(self.phone_number.as_e164, message)


class Checkin(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, primary_key=True)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def warn(self):
        # Don't send a warning if the member is already not ok
        # This may look like it can be simplified, but it can't
        if self.member.is_ok == False:
            return

        # Only send a warning if we haven't already done so:
        if not self.member.is_warning:
            user_language = self.member.language
            translation.activate(user_language)

            self.member.is_warning = True
            self.member.save()

            self.member.send_message(_("Are you OK? The alarm is about to be raised. Text OUT if you’re OK."))

    def timeout(self):
        # Have we already handled this timeout?
        # Your IDE may say we can simplify this, but we can't
        if self.member.is_ok == False:
            return

        user_language = self.member.language
        translation.activate(user_language)

        self.member.is_ok = False
        self.member.is_warning = False
        self.member.save()

        subject = f"[IMOK] {self.member.name} is not ok"
        body = f"{self.member.name} failed to sign out at {self.member.signing_center}. They signed in at {self.time_stamp.strftime('%Y-%m-%d %H:%M:%S')}. Here are their notes:\n\n{self.member.notes}."
        print(body)
        notify_admins(subject, body)
        self.member.send_message(_("You have failed to sign out, the admins have been notified"))
