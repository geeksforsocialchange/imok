import json

from behave import given, when, then
from django.db import transaction
from django.conf import settings
from freezegun import freeze_time
from dateutil import parser
import pytz

from application.models import Member, Checkin


@given(u'I have a telegram chat_id')
def step_impl(context):
    context.member.telegram_chat_id = 1
    context.member.save()


@given(u'I have a telegram username')
def step_impl(context):
    context.member.telegram_username = 'test_user'
    context.member.save()


@when(u'I send "{message}" via telegram at "{time}"')
def step_impl(context, message, time):
    dt = parser.parse(time).astimezone(tz=pytz.timezone(settings.TIME_ZONE))
    with freeze_time(dt):
        with transaction.atomic():
            context.response = context.test.client.post('/application/telegram',
                                                        telegram_message(message), content_type="application/json")
        context.test.assertEqual(context.response.status_code, 200)


@when(u'I send "{message}" via telegram')
def step_impl(context, message):
    with transaction.atomic():
        context.response = context.test.client.post('/application/telegram',
                                                    telegram_message(message), content_type="application/json")
        context.test.assertEqual(context.response.status_code, 200)


def telegram_message(message, username='test_user', chat_id=1):
    body = {
        "update_id": 12345678,
        "message": {
            "message_id": 12,
            "from": {
                "id": 1234567890,
                "is_bot": False,
                "first_name": "Alice",
                "username": username,
                "language_code": "en"
            },
            "chat": {
                "id": chat_id,
                "first_name": "Alice",
                "username": username,
                "type": "private"
            },
            "date": 1617365548,
            "text": message
        }
    }
    return body
