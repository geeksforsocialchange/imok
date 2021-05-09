from django.core.management.base import BaseCommand
from django.conf import settings
from application.models import Checkin
import django.utils.timezone as timezone


def healthcheck():
    warning_time = timezone.localtime() - settings.WARNING_TTL
    warning_checkins = Checkin.objects.filter(time_stamp__lte=warning_time).filter(member__warning_message_sent_at__isnull=True)
    for checkin in warning_checkins:
        checkin.warn()

    checkout_time = timezone.localtime() - settings.CHECKIN_TTL
    overdue_checkins = Checkin.objects.filter(time_stamp__lte=checkout_time).filter(member__overdue_message_sent_at__isnull=True)
    for checkin in overdue_checkins:
        checkin.timeout()

    return overdue_checkins.__len__(), warning_checkins.__len__()


class Command(BaseCommand):
    def handle(self, **options):
        print(healthcheck())
