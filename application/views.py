from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from twilio.twiml.messaging_response import MessagingResponse
from .models import Member
from django.utils.translation import gettext as _
from django.core import mail
from imok.settings import NOTIFY_EMAIL, MAIL_FROM


def index(_):
    return HttpResponseNotFound("hello world")


# @TODO verify this is from Twilio
@require_POST
@csrf_exempt
def twilio(request):
    message = request.POST
    if Member.objects.filter(phone_number=message['From']).count() != 1:
        mail.send_mail('SMS From Unknown Number', f"{message['From']} send {message['Body']}", MAIL_FROM, [NOTIFY_EMAIL])
        return HttpResponseNotFound('ERROR: User not found')

    command = message['Body'].split(' ')[0].upper()
    if command == 'YES' or command == 'Y':
        return register(message)
    elif command == 'IN' or command == 'I':
        return checkin(message)
    elif command == 'NAME':
        return name(message)
    elif command == 'SOS' or command == 'HELP':
        return sos(message)
    elif command == 'O' or command == 'OUT':
        return checkout(message)
    else:
        return HttpResponse('Invalid Command')


def register(message):
    sender = message['From']
    resp = MessagingResponse()
    member = Member.objects.get(phone_number=sender)
    member.registered = True
    member.save()

    response = " ".join([_("Thanks for registering, %(name)s!") % {'name': member.name},
                _("To sign in, text IN or I to this number."),
                _("To correct your name, text NAME followed by your name."),
                _("To get emergency help, text SOS or HELP.")
                ])

    resp.message(response)
    return HttpResponse(resp)


def name(message):
    sender = message['From']
    name = ' '.join(message['Body'].split(' ')[1:])
    member = Member.objects.get(phone_number=sender)
    member.name = name
    member.save()
    resp = MessagingResponse()
    response = _("You have set your name to %(name)s") % {'name': name}
    resp.message(response)
    return HttpResponse(resp)


def checkin(message):
    sender = message['From']
    resp = MessagingResponse()
    member = Member.objects.get(phone_number=sender)

    response = member.sign_in()

    resp.message(response)
    return HttpResponse(resp)


def checkout(message):
    sender = message['From']
    resp = MessagingResponse()
    member = Member.objects.get(phone_number=sender)

    response = member.sign_out()

    resp.message(response)
    return HttpResponse(resp)


def sos(message):
    sender = message['From']
    resp = MessagingResponse()
    member = Member.objects.get(phone_number=sender)
    response = member.handle_sos()
    resp.message(response)

    return HttpResponse(resp)
