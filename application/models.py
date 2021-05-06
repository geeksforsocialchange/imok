import pytz
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
import uuid
import logging

from django.utils import timezone
from django.utils.translation import gettext as _
from django.utils import translation
from django.core.exceptions import ValidationError, ImproperlyConfigured

from .telegram_group import TelegramGroup
from .metrics import MetricHour, increment_hourly_metric
from .twilio import twilio_send
from .telegram import telegram_send
from .contact_admins import notify_admins

from codename_generator import generator
import re

logger = logging.getLogger(__name__)

LANGUAGES = [('en_gb', 'English'), ('cy_GB', 'Welsh')]
SIGNING_CENTERS = [('dallas court', 'Dallas Court')]
SUPPORTED_CHANNELS = list(map(lambda c: (c, c.title()), settings.SUPPORTED_CHANNELS))


def validate_telegram_username(value):
    if value.startswith("@"):
        raise ValidationError(
            _('%(value)s should not include the "@"'),
            params={'value': value},
        )
    validator_regex = re.compile('[a-zA-Z0-9_]{5,32}')
    if not validator_regex.match(value):
        raise ValidationError(
            _('%(value)s is not a valid telegram username, valid usernames are 5 to 32 characters long containing letters, numers or _'),
            params={'value':value},
         )


def generate_codename():
    return '-'.join(generator())


class Member(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    codename = models.CharField(max_length=64, editable=False, null=True)
    name = models.CharField(default='', max_length=50)
    notes = models.TextField(default='', blank=True)
    registered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=5, choices=LANGUAGES, default='en_gb')
    registered = models.BooleanField(default=False)
    phone_number = PhoneNumberField(max_length=20, unique=True, null=True, blank=True,
                                    help_text="Enter a valid phone number (e.g. 0121 234 5678) or a number with an international call prefix.")
    signing_center = models.CharField(choices=SIGNING_CENTERS, default='dallas court', max_length=50)
    is_ok = models.BooleanField(null=True)
    is_warning = models.BooleanField(null=False, default=False)
    telegram_username = models.CharField(default='', unique=True, validators=[validate_telegram_username], blank=True, max_length=50, help_text="Without the initial '@'")
    telegram_chat_id = models.BigIntegerField(default=0)
    preferred_channel = models.CharField(choices=SUPPORTED_CHANNELS, default=settings.PREFERRED_CHANNEL, max_length=8,
                                         help_text="Which channel should the app contact the user via?")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.codename:
            # Generate codename once, then check the db. If exists, keep trying.
            self.codename = generate_codename()
            while Member.objects.filter(codename=self.codename).exists():
                self.codename = generate_codename()
        super(Member, self).save()

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
            response = _("Your check in time at %(center)s is %(in time)s.\n\nI will raise the alarm if you don't "
                         "check out by %(out time)s.\n\nI will update your check in time if you message IN again." % {
                             "center": self.signing_center,
                             "in time": str(in_time.time().strftime('%X')),
                             "out time": out_time.strftime('%X')
                         })
        else:
            response = _("You were already checked in.\n\nI updated your check in time to %(time)s." % {
                "time": in_time.time().strftime('%X')
            })
        return response

    def sign_out(self):
        self.is_ok = None
        self.is_warning = False
        self.save()

        try:
            checkin = Checkin.objects.get(member=self)
        except Checkin.DoesNotExist:
            # Translators: the uppercase commands need to remain in English
            return _("You were not checked in.\n\nTo check in, message IN.\n\nTo raise the alarm, message SOS.")
        checkin.delete()
        # Translators: feel free to change this to a similar sentiment in your culture
        return _("Your check out time from %(center)s is %(time)s.\n\nI hope you have a lovely day!") % {
            'center': self.signing_center,
            'time': str(timezone.localtime().time().strftime(
                '%H:%M:%S'))}

    def handle_sos(self):
        # Expression cannot be simplified as this is actually Optional[boolean]
        if self.is_ok == False:
            return

        # Flag the member as not ok
        self.is_ok = False
        self.save()

        # send notifications
        time = timezone.localtime()
        subject = f"[IMOK] {self.name} sent an SOS"
        if self.notes == "":
            notes = "There are no notes saved for this member"
        else:
            notes = f"Notes: {self.notes}"
        body = f"{self.name} ({self.phone_number}) sent an SOS at {self.signing_center}.\n\nThey raised it at {time.strftime('%H:%M')} on {time.strftime('%d/%m/%Y')}.\n\n{notes}."
        notify_admins(subject, body)
        return _("Thank you for letting me know.\n\nI notified the admins at %(time)s." % {
            "time": timezone.localtime().time().strftime('%X')})

    def send_message(self, message):
        if self.preferred_channel == 'TELEGRAM':
            if self.telegram_chat_id == 0:
                logger.error(f"Cannot message {self.telegram_username}, the member hasn't added the bot.")
                return
            telegram_send(self.telegram_chat_id, message)
        elif self.preferred_channel == 'TWILIO':
            twilio_send(self.phone_number.as_e164, message)
        else:
            raise ImproperlyConfigured("Member uses an unsupported channel")


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

            self.member.send_message(_("Have you forgotten to sign out? I am about to notify the admins.\n\nPlease "
                                       "send OUT if you have left %(signing center)s" % {
                                           "signing center": self.member.signing_center}))

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
        if self.member.notes == "":
            notes = "There are no notes saved for this member"
        else:
            notes = f"Notes: {self.member.notes}"
        body = f"{self.member.name} ({self.member.phone_number}) didn't sign out of {self.member.signing_center}.\n\nThey signed in at {self.time_stamp.strftime('%H:%M on %d/%m/%Y')}.\n\n{notes}."
        print(body)
        notify_admins(subject, body)
        self.member.send_message(_("You didn't check out of Government Facility.\n\nI notified the admins at %(time)s." % {"time": timezone.localtime().time().strftime('%X')}))

    def save(self, *args, **kwargs):
        increment_hourly_metric('checkin', self.member.signing_center)
        super(Checkin, self).save()

    def delete(self, *args, **kwargs):
        increment_hourly_metric('checkout', self.member.signing_center)
        super(Checkin, self).delete()
