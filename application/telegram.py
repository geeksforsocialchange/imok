from django.conf import settings
import requests
import json
from django.http import HttpResponse
from django.utils import translation
from .commands import handle_command

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

        # If the member's chat_id is zero then this is the first message we have received from them
        # Only updating chat_id once protects us against someone else claiming their username if it ever changes
        if member.telegram_chat_id == 0:
            member.telegram_chat_id = chat_id
            member.save()

        # Activate the correct language and pass the message through to handle_command
        with translation.override(member.language):
            response = handle_command(message_text, member)
            telegram_reply(chat_id, response)
    return HttpResponse('{}')
