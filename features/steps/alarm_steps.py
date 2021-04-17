from behave import given, when, then
from django.core import mail
from django.db import transaction
from django.utils import timezone
from freezegun import freeze_time
from dateutil import parser
from application.management.commands.healthcheck import healthcheck
import pytz

from application.models import Member, Checkin


def time_within(timestamp, timedelta):
    now = timezone.localtime()
    return now - timedelta < timestamp < now + timedelta


@when(u'I create a new member')
def step_impl(context):
    member = Member(phone_number='+12025550483', name="Fake User")
    member.save()
    context.member = member


@then(u'The member is not confirmed')
def step_impl(context):
    context.test.assertFalse(context.member.registered)


@then(u'The member was created recently')
def step_impl(context):
    context.test.assertTrue(time_within(context.member.registered_at, timezone.timedelta(seconds=10)))


@given(u'I have been registered as a member')
def step_impl(context):
    member = Member(phone_number='+12025550483', name="Fake User")
    member.save()
    context.member = member


@when(u'I send "{text}" via twilio at "{time}"')
def step_impl(context, text, time):
    with freeze_time(time):
        with transaction.atomic():
            context.response = context.test.client.post('/application/twilio',
                                                        {'From': context.member.phone_number, 'Body': text})
        context.test.assertEqual(context.response.status_code, 200)


@when(u'I send "{text}" via twilio')
def step_impl(context, text):
    with transaction.atomic():
        context.response = context.test.client.post('/application/twilio',
                                                    {'From': context.member.phone_number, 'Body': text})
        context.test.assertEqual(context.response.status_code, 200)


@then(u'My registration is confirmed')
def step_impl(context):
    # Create a new member object because we want to be able to compare to the original data
    member = Member.objects.get(id=context.member.id)
    context.test.assertTrue(member.registered)


@then(u'My registration time does not change')
def step_impl(context):
    member = Member.objects.get(id=context.member.id)
    context.test.assertEqual(member.registered_at, context.member.registered_at)


@then(u'My name is "{name}"')
def step_impl(context, name):
    member = Member.objects.get(id=context.member.id)
    context.test.assertEqual(name, member.name)


@given(u'My registration is confirmed')
def step_impl(context):
    context.member.registered = True
    context.member.save()


@then(u'I am checked in')
def step_impl(context):
    with transaction.atomic():
        count = Checkin.objects.filter(member=context.member).count()
    context.test.assertEqual(count, 1)


@then(u'I am not checked in')
def step_impl(context):
    with transaction.atomic():
        count = Checkin.objects.filter(member=context.member).count()
    context.test.assertEqual(count, 0)


@then(u'my check in record is deleted')
def step_impl(context):
    # The design of the system means that this is the same as "I am not checked in"
    with transaction.atomic():
        count = Checkin.objects.filter(member=context.member).count()
    context.test.assertEqual(count, 0)


@then(u'I receive a message containing "{message}"')
def step_impl(context, message):
    # @TODO handle languages
    content = str(context.response.content, 'utf-8')
    context.test.assertIn(message, content)


@given(u'I am not checked in')
def step_impl(context):
    try:
        Checkin.objects.get(member=context.member).delete()
    except Checkin.DoesNotExist:
        pass


@then(u'the check in time is "{time}"')
def step_impl(context, time):
    time = parser.parse(time).replace(tzinfo=pytz.timezone('UTC'))
    checkin = Checkin.objects.get(member=context.member)
    context.test.assertEqual(checkin.time_stamp, time)


@given(u'I am checked in at "{time}"')
def step_impl(context, time):
    with freeze_time(time):
        # @TODO consider moving member is_ok state to a function of checkin
        context.member.is_ok = True
        context.member.save()
        Checkin(member=context.member).save()


@when(u'the healthchecker runs at "{time}"')
def step_impl(context, time):
    with freeze_time(time):
        context.healthchecker = healthcheck()


@then(u'there are {some} overdue checkins')
def step_impl(context, some):
    count = context.healthchecker
    context.test.assertEqual(str(count[0]), some)


@then(u'there are {some} warning checkins')
def step_impl(context, some):
    count = context.healthchecker
    context.test.assertEqual(str(count[1]), some)


@then(u'I am not ok')
def step_impl(context):
    context.member.refresh_from_db()
    context.test.assertEqual(context.member.is_ok, False)


@then(u'I am ok')
def step_impl(context):
    context.member.refresh_from_db()
    context.test.assertTrue(context.member.is_ok)


@then(u'I might be ok')
def step_impl(context):
    context.member.refresh_from_db()
    context.test.assertIn(context.member.is_ok, [True, None])


@then(u'an admin is contacted')
def step_impl(context):
    context.test.assertEqual(len(mail.outbox), 1)
    context.test.assertEqual(mail.outbox[0].subject, "[IMOK] Fake User is not ok")
