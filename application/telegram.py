from imok.settings import TELEGRAM_TOKEN
import requests

BOT_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/'


def telegram_post(chat_id, message_text):
    response = {
        "chat_id": chat_id,
        "text": message_text
    }
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=response)
