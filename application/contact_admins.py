import requests

from django.core.mail import send_mail
from django.conf import settings

from .telegram_group import TelegramGroup


def notify_admins(subject, message):
    if settings.TELEGRAM_GROUP != '':
        # @TODO: Consolidate email and Telegram outputs
        # telegram_admins(subject + ":" + message)
        telegram_admins(message)
    if settings.NOTIFY_EMAIL != '':
        mail_admins(subject, message)


def mail_admins(subject, message):
    send_mail(subject,
              message,
              from_email=settings.MAIL_FROM,
              recipient_list=[settings.NOTIFY_EMAIL]
              )


# This looks suspiciously like telegram.telegram_reply() but using that would introduce a circular dependency
def telegram_admins(message):
    bot_url = f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/'
    group = TelegramGroup.objects.filter(title=settings.TELEGRAM_GROUP).first()
    response = {
        "chat_id": group.chat_id,
        "text": message
    }
    message_url = bot_url + 'sendMessage'
    r = requests.post(message_url, json=response)
    print(r.content)
    return '{}'
