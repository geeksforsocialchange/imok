from django.core.management.base import BaseCommand
from django.conf import settings
from application.models import Checkin
import django.utils.timezone as timezone
from phonenumbers.phonenumbermatcher import is_valid_number, is_possible_number
import phonenumbers


class Command(BaseCommand):
    def handle(self, **options):
        number = phonenumbers.parse("+447743917404", "GB")
        print(is_valid_number(number))
        print(is_possible_number(number))
