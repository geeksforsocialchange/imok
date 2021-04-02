from behave import given, when, then
from django.db import transaction
from django.core import mail
from django.contrib.auth.models import User
from faker import Faker
import phonenumbers

from application.models import Member, Checkin


def random_phone_number():
    fake = Faker(['en_GB'])
    number = phonenumbers.parse(fake.cellphone_number(), region='GB')
    return phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)


@given(u'email is configured')
def step_impl(context):
    from django.conf import settings
    context.test.assertEqual(settings.NOTIFY_EMAIL, 'root@localhost')


@given(u'{username} has logged in with an admin account')
def step_impl(context, username):
    user = User(username=username, is_staff=True, is_superuser=True)
    user.save()
    context.users[username] = user
    # @TODO actually login?


@when(u'{username} creates a new member')
def step_impl(context, username):
    member = Member(registered_by=context.users[username])
    member.save()
    context.member = member


@given(u'{membername} has been registered as a member')
def step_impl(context, membername):
    member = Member(name=membername, phone_number=random_phone_number())
    member.save()
    context.members[membername] = member


@given(u'has received a message containing <Welcome to imok!>')
def step_impl(context):
    pass


@when(u'{membername} replies <{text}>')
def step_impl(context, membername, text):
    member = context.members[membername]
    member.refresh_from_db()
    with transaction.atomic():
        context.response = context.test.client.post('/application/twilio',
                                                    {'From': member.phone_number, 'Body': text})
        context.test.assertEqual(context.response.status_code, 200)


@then(u'{membername}\'s registration is confirmed')
def step_impl(context, membername):
    member = context.members[membername]
    member.refresh_from_db()
    context.test.assertTrue(member.registered)


@then(u'{membername}\'s registration time does not change')
def step_impl(context, membername):
    member = context.members[membername]
    member.refresh_from_db()
    context.test.assertEqual(context.members[membername].registered_at, member.registered_at)


@given(u'{membername}\'s registration is confirmed')
def step_impl(context, membername):
    if membername in context.members:
        context.members[membername].registered = True
        context.members[membername].save()
    else:
        member = Member(name=membername, phone_number=random_phone_number())
        member.registered = True
        member.save()
        context.members[membername] = member


# @TODO this only tests that username has any permissions in 'application'
# This works because we use superadmin users everywhere at the moment
@then(u'{username} can see that {membername}\'s account registration was confirmed')
def step_impl(context, username, membername):
    user = context.users[username]
    user.has_module_perms('application')


@given(u'An unknown number messages the imok number <{text}>')
def step_impl(context, text):
    with transaction.atomic():
        context.response = context.test.client.post('/application/twilio', {'From': random_phone_number(), 'Body': text})
        context.test.assertEqual(context.response.status_code, 404)


@then(u'No response is sent')
def step_impl(context):
    content = str(context.response.content, 'utf-8')
    context.test.assertIn('ERROR', content)


@then(u'the admins are emailed')
def step_impl(context):
    context.test.assertEqual(len(mail.outbox), 1)
    context.test.assertEqual(mail.outbox[0].subject, "SMS From Unknown Number")
