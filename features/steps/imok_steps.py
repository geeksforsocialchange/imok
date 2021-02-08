from behave import given, when, then
from django.db import transaction
from django.utils import timezone

from application.models import Member, Checkin


def time_within(timestamp, timedelta):
    now = timezone.now()
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


@when(u'I reply <{text}>')
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


@then(u'My name is <{name}>')
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


@then(u'I receive a message containing <{message}>')
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
