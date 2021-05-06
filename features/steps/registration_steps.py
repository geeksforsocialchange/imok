from behave import given, when, then
from django.db import transaction
from django.conf import settings
from django.core import mail
from django.contrib.auth.models import User
from dateutil import parser
from freezegun import freeze_time
import pytz


from application.models import Member


@given(u'email is configured')
def step_impl(context):
    from django.conf import settings
    context.test.assertEqual(settings.NOTIFY_EMAIL, 'root@localhost')


@given(u'{username} has logged in with an admin account')
def step_impl(context, username):
    user = User(username=username, is_staff=True, is_superuser=True)
    user.save()
    context.users[username] = user


@when(u'{username} creates a new member')
def step_impl(context, username):
    member = Member(registered_by=context.users[username])
    member.save()
    context.member = member


@given(u'{membername} has been registered as a member')
def step_impl(context, membername):
    member = Member(name=membername, phone_number='+447740000000')
    member.save()
    context.members[membername] = member

@given(u'{membername}\'s signing center is {location}')
def step_impl(context, membername, location):
    context.members[membername].signing_center = location
    context.members[membername].save()


@given(u'has received a message containing <Welcome to imok!>')
def step_impl(context):
    pass


@when(u'{membername} replies <{text}> at "{time}"')
def step_impl(context, membername, text, time):
    dt = parser.parse(time).astimezone(tz=pytz.timezone(settings.TIME_ZONE))
    with freeze_time(dt):
        member = context.members[membername]
        member.refresh_from_db()
        with transaction.atomic():
            context.response = context.test.client.post('/application/twilio',
                                                        {'From': member.phone_number, 'Body': text})
            context.test.assertEqual(context.response.status_code, 200)


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
        member = Member(name=membername, phone_number='+447740000000')
        member.registered = True
        member.save()
        context.members[membername] = member


@then(u'{username} can see that {membername}\'s account registration was confirmed')
def step_impl(context, username, membername):
    user = context.users[username]
    user.has_module_perms('application')


@given(u'An unknown number messages the imok number <{text}>')
def step_impl(context, text):
    with transaction.atomic():
        context.response = context.test.client.post('/application/twilio', {'From': '+447740000001', 'Body': text})
        context.test.assertEqual(context.response.status_code, 404)


@then(u'No response is sent')
def step_impl(context):
    content = str(context.response.content, 'utf-8')
    context.test.assertIn('ERROR', content)


@then(u'the admins are emailed')
def step_impl(context):
    context.test.assertEqual(len(mail.outbox), 1)
    context.test.assertEqual(mail.outbox[0].subject, "SMS From Unknown Number")


@then(u'{member} receives a message containing')
def step_impl(context, member):
    content = str(context.response.content, 'utf-8')
    context.test.assertIn(context.text, content)


@then(u'{admin} recieves a message in a Telegram group containing: "{content}"')
def step_impl(context, admin, content):
    context.test.assertEqual(len(mail.outbox), 1)
    context.test.assertIn(content, mail.outbox[0].body)
