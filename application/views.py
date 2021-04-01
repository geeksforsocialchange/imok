from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .twilio import validate_twilio_request, twilio_receive
from .telegram import telegram_receive


# @TODO all this does at the moment is reply to private messages with what was sent
@csrf_exempt
@require_POST
def telegram(request):
    return telegram_receive(request)


# @TODO move this to twilio.py and refactor all other commands to be independent of channel
@validate_twilio_request
@require_POST
@csrf_exempt
def twilio(request):
    return twilio_receive(request)


