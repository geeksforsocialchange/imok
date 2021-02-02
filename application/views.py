from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from twilio.twiml.messaging_response import MessagingResponse
from .models import Subscriber, Checkin, Invite


def index(request):
    return HttpResponse("Hello, world. You're at the API index")


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

        resp.message("Thank you for registering, please now tell us what to do if you disappear by sending 'NOTES' followed by some notes.")
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
        resp.message("You have checked in")
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
            resp.message("You have now checked out")
        else:
            resp.message("You were not checked in")
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
    resp.message("Thank you.  You may now use the service by sending 'IN' to checkin  and 'OUT' to checkout")
    return HttpResponse(resp)
