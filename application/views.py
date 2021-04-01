from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from twilio.twiml.messaging_response import MessagingResponse
from .models import Member
from django.utils.translation import gettext as _
from django.core import mail
from imok.settings import NOTIFY_EMAIL, MAIL_FROM, TWILIO_AUTH_TOKEN, DEBUG
from django.utils import translation
from twilio.request_validator import RequestValidator
from functools import wraps
from .telegram import telegram_post
import json


def index(_):
    return HttpResponseNotFound("hello world")


@csrf_exempt
@require_POST
def telegram(request):
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
        telegram_post(chat_id, message_text)
    return HttpResponse('{}')


def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(TWILIO_AUTH_TOKEN)

        url = request.build_absolute_uri()
        from urllib.parse import urlsplit, urlunsplit
        url = list(urlsplit(url))
        url[0] = request.META.get('HTTP_X_FORWARDED_PROTO', 'http')
        url[1] = f"{request.META.get('HTTP_HOST')}:{request.META.get('HTTP_X_FORWARDED_PORT', 80)}"
        original_url = urlunsplit(url)

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            original_url,
            request.POST,
            request.META.get('HTTP_X_TWILIO_SIGNATURE', ''))

        # Continue processing the request if it's valid, return a 403 error if
        # it's not
        if request_valid or DEBUG:
            return f(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return decorated_function


@validate_twilio_request
@require_POST
@csrf_exempt
def twilio(request):
    message = request.POST
    if Member.objects.filter(phone_number=message['From']).count() != 1:
        mail.send_mail('SMS From Unknown Number', f"{message['From']} send {message['Body']}", MAIL_FROM, [NOTIFY_EMAIL])
        return HttpResponseNotFound('ERROR: User not found')

    member = Member.objects.get(phone_number=message['From'])
    user_language = member.language
    translation.activate(user_language)

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
