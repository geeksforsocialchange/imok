from django.core.management.base import BaseCommand
from django.conf import settings
from application.models import Checkin
import django.utils.timezone as timezone


def healthcheck():
    checkout_time = timezone.localtime() - settings.CHECKIN_TTL
    checkins = Checkin.objects.filter(time_stamp__lte=checkout_time)
    for checkin in checkins:
        checkin.timeout()

    warning_time = timezone.localtime() - settings.WARNING_TTL
    warning_checkins = Checkin.objects.filter(time_stamp__lte=warning_time)
    for checkin in warning_checkins:
        checkin.warn()

    return checkins.__len__(), warning_checkins.__len__()


class Command(BaseCommand):
    def handle(self, **options):
        print(healthcheck())
