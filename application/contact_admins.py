import requests
import logging

from django.core.mail import send_mail
from django.conf import settings

from .telegram_group import TelegramGroup

logger = logging.getLogger(__name__)


def notify_admins(subject, message):
    try:
        telegram_admins(message)
    except:
        logger.warning("Failed to send notification to Telegram group")
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
    group = TelegramGroup.objects.first()
    response = {
        "chat_id": group.chat_id,
        "text": message,
    }
    message_url = bot_url + 'sendMessage'
    r = requests.post(message_url, json=response)
    print(r.content)
    return '{}'
