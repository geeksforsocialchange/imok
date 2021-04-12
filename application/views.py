from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
import json
import logging

from .twilio import validate_twilio_request, twilio_receive
from .telegram import telegram_receive
from .models import Member, TelegramGroup
from .contact_admins import notify_admins
from imok.settings import TELEGRAM_GROUP


logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def telegram(request):
    body = json.loads(request.body)
    if 'my_chat_member' in body.keys():
        if body['my_chat_member']['chat']['title'] == TELEGRAM_GROUP:
            TelegramGroup.objects.update_or_create(chat_id=body['my_chat_member']['chat']['id'], defaults={'title': TELEGRAM_GROUP})
            return HttpResponse('{}')
        else:
            logger.error("Somebody invited the Telegram bot into an unknown group")
            return HttpResponseBadRequest('{"error": "bad telegram group"}')
    try:
        username = body['message']['from']['username']
    except (TypeError, KeyError):
        return HttpResponse()
    member = Member.objects.get(telegram_username=username)
    return telegram_receive(request, member)


@validate_twilio_request
@require_POST
@csrf_exempt
def twilio(request):
    message = request.POST
    if Member.objects.filter(phone_number=message['From']).count() != 1:
        logger.error(f"SMS from unkown number {message['From']}")
        notify_admins('SMS From Unknown Number', f"{message['From']} send {message['Body']}")
        return HttpResponseNotFound('ERROR: User not found')

    member = Member.objects.get(phone_number=message['From'])
    return twilio_receive(request, member)


