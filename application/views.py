from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from twilio.twiml.messaging_response import MessagingResponse
from .models import Subscriber, Checkin, Invite
from django.utils.translation import gettext as _


def index(request):
    return HttpResponseNotFound("hello world")


# @TODO verify this is from Twilio
@require_POST
@csrf_exempt
def twilio(request):
    message = request.POST
    command = message['Body'].split(' ')[0].upper()
    if command == 'IN':
        return checkin(message)
    elif command == 'OUT':
        return checkout(message)
    elif command == 'NAME':
        return subscribe(message)
    elif command == 'NOTES':
        return notes(message)
    else:
        return HttpResponse("Invalid command")


def subscribe(message):
    sender = message['From']
    name = ' '.join(message['Body'].split(' ')[1:])
    if Invite.objects.filter(phone_number=sender).count() == 1:
        resp = MessagingResponse()
        subscriber = Subscriber(phone_number=sender, name=name)
        subscriber.save()

        invite = Invite.objects.get(phone_number=sender)
        invite.delete()
        # Translators: This message is sent when a user has registered
        response = _("Thank you for registering, please now tell us what to do if you disappear by sending 'NOTES' followed by some notes.")
        resp.message(response)
        return HttpResponse(resp)
    else:
        return HttpResponse({})


def checkin(message):
    sender = message['From']
    if Subscriber.objects.filter(phone_number=sender).count() == 1:
        resp = MessagingResponse()
        subscriber = Subscriber.objects.get(phone_number=sender)
        checkin = Checkin(phone_number=subscriber)
        checkin.save()
        # Translators: this is sent when a user successfully checks in
        response = _("You have checked in")
        resp.message(response)
    else:
        resp = {}
    return HttpResponse(resp)


def checkout(message):
    sender = message['From']
    if Subscriber.objects.filter(phone_number=sender).count() == 1:
        resp = MessagingResponse()
        if Checkin.objects.filter(phone_number=sender).count() == 1:
            checkin = Checkin.objects.get(phone_number=sender)
            checkin.delete()
            # Translators: this is sent to confirm a user has successfully checked out
            response = _("You have now checked out")
            resp.message(response)
        else:
            # Translators: this is sent when a user tries to check out but wasn't checked in
            response = _("You were not checked in")
            resp.message(response)
    else:
        resp = {}
    return HttpResponse(resp)


def notes(message):
    sender = message['From']
    notes = ' '.join(message['Body'].split(' ')[1:])
    resp = MessagingResponse()
    subscriber = Subscriber.objects.get(phone_number=sender)
    subscriber.notes = notes
    subscriber.save()
    # Translators: This is sent once a user is fully registered
    response = _("Thank you.  You may now use the service by sending 'IN' to checkin  and 'OUT' to checkout")
    resp.message(response)
    return HttpResponse(resp)
