from django.core.management.base import BaseCommand
from application.models import Checkin
from imok.settings import CHECKIN_TTL
import django.utils.timezone as timezone


def healthcheck():
    # @TODO handle reminder to checkout
    time = timezone.now() - CHECKIN_TTL
    checkins = Checkin.objects.filter(time_stamp__lte=time)
    for checkin in checkins:
        checkin.timeout()
    return checkins.__len__()


class Command(BaseCommand):
    def handle(self, **options):
        print(healthcheck())
