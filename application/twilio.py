from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from functools import wraps
from django.conf import settings
from django.http import HttpResponseForbidden, HttpResponse
from django.utils import translation
from .commands import handle_command


def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)

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
        if request_valid or settings.DEBUG is True:
            return f(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return decorated_function


def twilio_receive(request, member):
    message = request.POST

    user_language = member.language
    translation.activate(user_language)

    message_body = message['Body']
    reply = handle_command(message_body, member)

    resp = MessagingResponse()
    resp.message(reply)
    return HttpResponse(resp)


def twilio_send(phone_number, message):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=message,
        from_=settings.TWILIO_FROM_NUMBER,
        to=phone_number
    )
    print(message.sid)
