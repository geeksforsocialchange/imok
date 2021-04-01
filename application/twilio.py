from twilio.request_validator import RequestValidator
from functools import wraps
from django.http import HttpResponseForbidden
from imok.settings import TWILIO_AUTH_TOKEN, DEBUG


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
