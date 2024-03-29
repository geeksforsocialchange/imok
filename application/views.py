from django.db.utils import ProgrammingError
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.template import loader
import json
import logging

from os import getenv
import re

from .twilio import validate_twilio_request, twilio_receive
from .telegram import telegram_receive, telegram_reply
from .telegram_botinfo import get_me
from .models import Member, TelegramGroup
from .contact_admins import notify_admins

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def telegram(request):
    print(request.body)
    body = json.loads(request.body)
    if 'my_chat_member' in body.keys():
        # The bot was added/removed from a group (or blocked/unblocked by someone)
        if TelegramGroup.objects.count() == 0:
            # Register the chat_id of the group that the bot just got added to
            # but only if the bot isn't already in a group
            TelegramGroup.objects.create(chat_id=body['my_chat_member']['chat']['id'], title='admin')
            return HttpResponse('{}')
        else:
            logger.warning("Received a group membership event, but we already have a group saved")
            return HttpResponse('{"error": "bad telegram group"}')
    try:
        # Try and get a username from the Telegram event
        username = body['message']['from']['username']
    except (TypeError, KeyError):
        # If there's no username and it's not a join event, then it's not something we care about
        return HttpResponse()
    try:
        # Find the member with this telegram username
        member = Member.objects.get(telegram_username=username)
        # Pass the event through to telegram_receive() and do something with it
        return telegram_receive(request, member)
    except(Member.DoesNotExist):
        # If we've got this far then the Telegram event is probably from a member that we don't know about
        # @TODO we should create the member here if registrations aren't required
        telegram_reply(body['message']['chat']['id'], "Your username is not registered with imok")
        return HttpResponse('{}')


@validate_twilio_request
@require_POST
@csrf_exempt
def twilio(request):
    message = request.POST
    from_number = message['From'].replace("whatsapp:", "")  # handle whatsapp by stripping the prefix before a lookup
    if Member.objects.filter(phone_number=from_number).count() != 1:
        logger.error(f"SMS from unknown number {message['From']}")
        notify_admins('SMS From Unknown Number', f"{message['From']} send {message['Body']}")
        return HttpResponseNotFound('ERROR: User not found')

    member = Member.objects.get(phone_number=message['From'])
    return twilio_receive(request, member)


def varz(request):
    chat_id = telegram_group_chat_id()
    if request.user.is_superuser:
        response = [{'key': 'ALLOWED_HOSTS', 'value': settings.ALLOWED_HOSTS, 'validation': None},
                    {'key': 'TWILIO_ACCOUNT_SID', 'value': redact(settings.TWILIO_ACCOUNT_SID), 'validation': len(settings.TWILIO_ACCOUNT_SID) == 34},
                    {'key': 'TWILIO_AUTH_TOKEN', 'value': redact(settings.TWILIO_AUTH_TOKEN), 'validation': None},
                    {'key': 'TELEGRAM_TOKEN', 'value': redact(settings.TELEGRAM_TOKEN), 'validation': get_me()['ok']},
                    {'key': 'Telegram Group chat_id', 'value': chat_id, 'validation': type(chat_id) == int, 'solution': "" if type(chat_id) == int else "re-add the bot to the group"},
                    {'key': 'DOKKU_LETSENCRYPT_EMAIL', 'value': getenv('DOKKU_LETSENCRYPT_EMAIL'), 'validation': getenv('DOKKU_LETSENCRYPT_EMAIL') is not None},
                    {'key': 'NOTIFY_EMAIL', 'value': getenv('NOTIFY_EMAIL'), 'validation': getenv('NOTIFY_EMAIL') is not None},
                    {'key': 'MAIL_FROM', 'value': getenv('MAIL_FROM'), 'validation': getenv('MAIL_FROM') is not None},
                    {'key': 'EMAIL_HOST', 'value': settings.EMAIL_HOST, 'validation': None},
                    {'key': 'EMAIL_PORT', 'value': settings.EMAIL_PORT, 'validation': None},
                    {'key': 'EMAIL_USE_TLS', 'value': settings.EMAIL_USE_TLS, 'validation': None},
                    {'key': 'EMAIL_HOST_USER', 'value': settings.EMAIL_HOST_USER, 'validation': None},
                    {'key': 'EMAIL_HOST_PASSWORD', 'value': redact(settings.EMAIL_HOST_PASSWORD), 'validation': None},
                    {'key': 'CHECKIN_TTL', 'value': settings.CHECKIN_TTL, 'validation': None},
                    {'key': 'WARNING_TTL', 'value': settings.WARNING_TTL, 'validation': None},
                    {'key': 'PHONENUMBER_DEFAULT_REGION', 'value': settings.PHONENUMBER_DEFAULT_REGION, 'validation': None},
                    {'key': 'SUPPORTED_CHANNELS', 'value': settings.SUPPORTED_CHANNELS, 'validation': None},
                    {'key': 'PREFERRED_CHANNEL', 'value': settings.PREFERRED_CHANNEL, 'validation': None},
                    {'key': 'REQUIRE_INVITE', 'value': settings.REQUIRE_INVITE, 'validation': None},
                    {'key': 'STATIC_ROOT', 'value': settings.STATIC_ROOT, 'validation': None},
                    {'key': 'DEBUG', 'value': settings.DEBUG, 'validation': settings.DEBUG is False},
                    {'key': 'LANGUAGES', 'value': settings.LANGUAGES, 'validation': None},
                    {'key': 'SECRET_KEY', 'value': redact(settings.SECRET_KEY), 'validation': settings.SECRET_KEY==getenv('SECRET_KEY')}
                    ]
        if hasattr(settings, 'AIRBRAKE_PROJECT'):
            response.append({'key': 'AIRBRAKE_PROJECT', 'value': redact(settings.AIRBRAKE_PROJECT), 'validation': None})
            if hasattr(settings, 'AIRBRAKE_PROJECT_KEY'):
                response.append({'key': 'AIRBRAKE_PROJECT_KEY', 'value': redact(settings.AIRBRAKE_PROJECT_KEY), 'validation': None})
            else:
                response.append({'key': 'AIRBRAKE_PROJECT_KEY', 'value': None, 'validation': False})
        else:
            response.append({'key': 'AIRBRAKE_PROJECT', 'value': None, 'validation': None})

        template = loader.get_template('varz.html')
        context = {
            'varz': response,
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseForbidden('{"ERROR": "Not authenticated"}')


def telegram_group_chat_id():
    try:
        return TelegramGroup.objects.get().chat_id
    except TelegramGroup.DoesNotExist:
        return "unknown"
    except ProgrammingError:
        return "database error"
    except:
        return "unknown error"


def redact(string):
    string = str(string)
    if len(string) < 4:
        return re.sub(r".", "*", string)
    first_char = string[0]
    last_char = string[-1]
    modified_str = re.sub(r".", "*", string[1:-1])
    return first_char + modified_str + last_char
