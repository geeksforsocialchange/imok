from django.conf import settings
from django.core.management.base import BaseCommand
import django.utils.timezone as timezone

from application.models import Checkin


class Command(BaseCommand):
    def handle(self, **options):
        time = timezone.now() - settings.CHECKIN_TTL
        checkins = list(Checkin.objects.filter(time_stamp__lte=time))
        if len(checkins) == 0:
            print("There are no overdue checkouts")
        for checkin in checkins:
            print(f"{checkin.member.name} checked in at {checkin.time_stamp}")
