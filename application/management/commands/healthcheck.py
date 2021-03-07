from django.core.management.base import BaseCommand
from application.models import Checkin
from imok.settings import CHECKIN_TTL, NOTIFY_EMAIL
import django.utils.timezone as timezone
from django.core.mail import send_mail


def healthcheck():
    # @TODO handle reminder to checkout
    time = timezone.now() - CHECKIN_TTL
    checkins = Checkin.objects.filter(time_stamp__lte=time)
    for checkin in checkins:
        handle_checkin_fail(checkin)
    return checkins.__len__()


def handle_checkin_fail(checkin):
    # Expression cannot be simplified as this is actually Optional[boolean]
    if checkin.member.is_ok == False:
        return

    # Flag the member as not ok
    checkin.member.is_ok = False
    checkin.member.save()

    # send an email
    subject = f"[IMOK] {checkin.member.name} is not ok"
    body = f"{checkin.member.name} failed to sign out at {checkin.member.signing_center}. They signed in at {checkin.time_stamp}. Here are their notes:\n\n{checkin.member.notes}."
    send_mail(subject,
              body,
              from_email="noreply@imok.wheresalice.info",  # @TODO make this configurable
              recipient_list=[NOTIFY_EMAIL]  # @TODO make this configurable
              )


def handle_sos(member):
    # Expression cannot be simplified as this is actually Optional[boolean]
    if member.is_ok == False:
        return

    # Flag the member as not ok
    member.is_ok = False
    member.save()

    # send an email
    subject = f"[IMOK] {member.name} sent an SOS"
    body = f"{member.name} sent an SOS from {member.signing_center}.  Here are their notes:\n\n{member.notes}."
    send_mail(subject,
              body,
              from_email="noreply@imok.wheresalice.info",  # @TODO make this configurable
              recipient_list=[NOTIFY_EMAIL]  # @TODO make this configurable
              )


class Command(BaseCommand):
    def handle(self, **options):
        print(healthcheck())
