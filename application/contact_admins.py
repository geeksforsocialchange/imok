from django.core.mail import send_mail

from django.conf import settings
from .telegram import telegram_send


def notify_admins(subject, message):
    if settings.TELEGRAM_GROUP != '':
        telegram_admins(message)
    if settings.NOTIFY_EMAIL != '':
        mail_admins(subject, message)


def mail_admins(subject, message):
    send_mail(subject,
              message,
              from_email=settings.MAIL_FROM,
              recipient_list=[settings.NOTIFY_EMAIL]
              )


def telegram_admins(message):
    telegram_send(settings.TELEGRAM_GROUP, message)
