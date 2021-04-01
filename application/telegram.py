from imok.settings import TELEGRAM_TOKEN, NOTIFY_EMAIL
import requests
import json
from django.http import HttpResponse
from django.utils import translation
from .models import Member
from .commands import handle_command

BOT_URL = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/'


def telegram_reply(chat_id, message_text):
    response = {
        "chat_id": chat_id,
        "text": message_text
    }
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=response)


def telegram_receive(request):
    body = json.loads(request.body)

    # Do nothing with group invites:
    if 'my_chat_member' in body.keys():
        return HttpResponse('{}')
    # Do nothing with messages in group chat:
    if body['message']['chat']['type'] == 'group':
        return HttpResponse('{}')

    # Only respond to private messages:
    if body['message']['chat']['type'] == 'private':
        chat_id = body['message']['chat']['id']
        message_text = body['message']['text']

        member = Member.objects.get(telegram_username=body['from']['username'])
        user_language = member.language
        translation.activate(user_language)
        response = handle_command(message_text, member)
        telegram_reply(chat_id, response)
    return HttpResponse('{}')
