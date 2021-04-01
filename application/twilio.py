from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse
from functools import wraps
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponse
from django.core import mail
from django.utils import translation
from imok.settings import TWILIO_AUTH_TOKEN, DEBUG, MAIL_FROM, NOTIFY_EMAIL
from .models import Member
from .commands import handle_command


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


def twilio_receive(request):
    message = request.POST
    if Member.objects.filter(phone_number=message['From']).count() != 1:
        mail.send_mail('SMS From Unknown Number', f"{message['From']} send {message['Body']}", MAIL_FROM, [NOTIFY_EMAIL])
        return HttpResponseNotFound('ERROR: User not found')

    member = Member.objects.get(phone_number=message['From'])
    user_language = member.language
    translation.activate(user_language)

    message_body = message['Body']
    reply = handle_command(message_body, member)

    resp = MessagingResponse()
    resp.message(reply)
    return HttpResponse(resp)

