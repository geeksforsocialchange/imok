from logging import getLogger
from os import getenv
import re

from django.conf import settings
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden

from application.models import Member

logger = getLogger('django')


def index(request):
    if Member.objects.count() == 0:
        return HttpResponse("Welcome to imok. You're probably looking for the <a href='/ruok'>admin screen.</a>")
    else:
        return HttpResponse("")


def healthz(request):
    if database_ok():
        return HttpResponse("OK")


def varz(request):
    if request.user.is_superuser:
        response = {
            'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
            'TWILIO_ACCOUNT_SID': redact(settings.TWILIO_ACCOUNT_SID),
            'TWILIO_AUTH_TOKEN': redact(settings.TWILIO_AUTH_TOKEN),
            'TWILIO_FROM_NUMBER': redact(settings.TWILIO_FROM_NUMBER),
            'TELEGRAM_TOKEN': redact(settings.TELEGRAM_TOKEN),
            'TELEGRAM_GROUP': redact(settings.TELEGRAM_TOKEN),
            'DOKKU_LETSENCRYPT_EMAIL': getenv('DOKKU_LETSENCRYPT_EMAIL'),
            'NOTIFY_EMAIL': redact(getenv('NOTIFY_EMAIL')),
            'MAIL_FROM': redact(getenv('MAIL_FROM')),
            'EMAIL_HOST': getenv('EMAIL_HOST'),
            'EMAIL_PORT': getenv('EMAIL_PORT'),
            'EMAIL_USE_TLS': getenv('EMAIL_USE_TLS'),
            'EMAIL_HOST_USER': redact(getenv('EMAIL_HOST_USER')),
            'EMAIL_HOST_PASSWORD': redact(getenv('EMAIL_HOST_PASSWORD'))
        }
        if hasattr(settings, 'AIRBRAKE_PROJECT'):
            response['AIRBRAKE_PROJECT'] = redact(settings.AIRBRAKE_PROJECT)
            response['AIRBRAKE_PROJECT_KEY'] = redact(settings.AIRBRAKE_PROJECT_KEY)
        return JsonResponse(response)
    else:
        return HttpResponseForbidden('{"ERROR": "Not authenticated"}')


def redact(string):
    string = str(string)
    if len(string) < 4:
        return re.sub(r".", "*", string)
    first_char = string[0]
    last_char = string[-1]
    modified_str = re.sub(r".", "*", string[1:-1])
    return first_char + modified_str + last_char


def database_ok():
    try:
        from django.db import connections
    except ImportError as e:
        logger.exception(e)
        return False

    try:
        for name in connections:
            cursor = connections[name].cursor()
            cursor.execute("SELECT 1;")
            row = cursor.fetchone()
            if row is None:
                return False
    except Exception as e:
        logger.exception(e)
        return False
    else:
        return True
