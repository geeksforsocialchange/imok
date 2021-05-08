from django.conf import settings
from django.core.cache import cache
import requests

BOT_URL = f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/'


def get_me():
    r = requests.get(BOT_URL + 'getMe')
    return r.json()


def bot_link():
    telegram_link = cache.get('telegram_link')
    if not telegram_link:
        r = get_me()
        try:
            telegram_link = f"https://t.me/{r['result']['username']}"
            cache.set('telegram_link', telegram_link, 3600)
        except KeyError:
            telegram_link = None
    return telegram_link
