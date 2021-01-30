from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from twilio.twiml.messaging_response import MessagingResponse
import json
from .models import Subscriber, Checkin


def index(request):
    return HttpResponse("Hello, world. You're at the API index")


# @TODO verify this is from Twilio
@require_POST
@csrf_exempt
def twilio(request):
    message = json.loads(request.body)
    # @TODO break this into separate functions for check-in and check-out
    if Subscriber.objects.filter(phone_number=message['From']).count() == 1:
        resp = MessagingResponse()
        if message['Body'].upper() == 'IN':
            u = Subscriber.objects.get(pk=message['From'])
            u.checkin_set.create()
            body = "You have checked in"
        else:
            body = f"We didn't understand {message['Body']}"
        resp.message(body)
    else:
        # User didn't exist
        resp = {}
    # Return the TwiML
    return HttpResponse(resp)
