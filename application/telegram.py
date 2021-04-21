from django.conf import settings
import requests
import json
from django.http import HttpResponse
from django.utils import translation
from .commands import handle_command
from imok.settings import TELEGRAM_GROUP

BOT_URL = f'https://api.telegram.org/bot{settings.TELEGRAM_TOKEN}/'



def telegram_reply(chat_id, message_text):
    response = {
        "chat_id": chat_id,
        "text": message_text
    }
    message_url = BOT_URL + 'sendMessage'
    r = requests.post(message_url, json=response)
    print(r.content)
    return '{}'


def telegram_send(chat_id, message_text):
    if chat_id == 0:
        raise Exception("chat_id cannot be zero")
    return telegram_reply(chat_id=chat_id, message_text=message_text)


def telegram_receive(request, member):
    body = json.loads(request.body)

    # Do nothing with messages in group chat:
    if body['message']['chat']['type'] == 'group':
        return HttpResponse('{}')

    # Only respond to private messages:
    if body['message']['chat']['type'] == 'private':
        chat_id = body['message']['chat']['id']
        message_text = body['message']['text']

        member.telegram_chat_id = chat_id
        member.save()

        user_language = member.language
        translation.activate(user_language)
        response = handle_command(message_text, member)
        telegram_reply(chat_id, response)
    return HttpResponse('{}')
