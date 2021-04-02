from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseNotFound
import json

from .twilio import validate_twilio_request, twilio_receive
from .telegram import telegram_receive
from .models import Member
from .contact_admins import notify_admins


@csrf_exempt
@require_POST
def telegram(request):
    body = json.loads(request.body)
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
        notify_admins('SMS From Unknown Number', f"{message['From']} send {message['Body']}")
        return HttpResponseNotFound('ERROR: User not found')

    member = Member.objects.get(phone_number=message['From'])
    return twilio_receive(request, member)


