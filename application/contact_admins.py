from django.core.mail import send_mail

from django.conf import settings
from .telegram import telegram_send
from .telegram_group import TelegramGroup


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
    group = TelegramGroup.objects.filter(title=settings.TELEGRAM_GROUP).first()
    telegram_send(group.chat_id, message)
