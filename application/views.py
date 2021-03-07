from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from twilio.twiml.messaging_response import MessagingResponse
from .models import Member, Checkin
from django.utils.translation import gettext as _
from django.utils import timezone
from imok.settings import CHECKIN_TTL
from application.management.commands import healthcheck

def index(_):
    return HttpResponseNotFound("hello world")


# @TODO verify this is from Twilio
@require_POST
@csrf_exempt
def twilio(request):
    message = request.POST
    if Member.objects.filter(phone_number=message['From']).count() != 1:
        return HttpResponse('User not found')

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
    member = Member.objects.filter(phone_number=sender).get()
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
    in_time = timezone.now()
    out_time = in_time + CHECKIN_TTL
    resp = MessagingResponse()
    member = Member.objects.get(phone_number=sender)

    member.is_ok = True
    member.save()

    checkin, created = Checkin.objects.update_or_create(member=member, defaults={'time_stamp': in_time})
    if created:
        response = " ".join([
                 _("You were checked in at %(center)s at %(time)s") % {'center': member.signing_center, 'time': str(in_time.time())},
                 _("We will alert our team if we don’t hear from you by %(time)s") % {'time': out_time}
                 ])
    else:
        response = _("You were already checked in. Your check in time has been updated")

    resp.message(response)
    return HttpResponse(resp)


def checkout(message):
    sender = message['From']
    resp = MessagingResponse()
    member = Member.objects.get(phone_number=sender)

    member.is_ok = None
    member.save()

    try:
        checkin = Checkin.objects.get(member=member)
    except Checkin.DoesNotExist:
        response = _("You were not checked in. To check in message IN")
        resp.message(response)
        return HttpResponse(resp)
    checkin.delete()
    response = _("You were checked out at %(center)s at %(time)s") % {'center': member.signing_center, 'time': str(timezone.now().time())}
    resp.message(response)
    return HttpResponse(resp)


def sos(message):
    sender = message['From']
    resp = MessagingResponse()
    member = Member.objects.get(phone_number=sender)
    healthcheck.handle_sos(member)
    response = _("Thanks for letting us know, our staff have been notified")
    resp.message(response)

    return HttpResponse(resp)
