from behave import given, when, then

from application.models import Member, Checkin
from application.commands import handle_command
from django.utils import translation


@given(u'I have been registered as a member who speaks {language}')
def step_impl(context, language):
    member = Member(phone_number='+12025550483', name="Fake User", language=language)
    member.save()
    print(member.language)
    translation.activate(member.language)
    context.member = member


@when(u'I send the command {command}')
def step_impl(context, command):
    context.response = handle_command(command, context.member)


@then(u'it returns {response}')
def step_impl(context, response):
    context.test.assertEqual(translation.get_language(), context.member.language)
    context.test.assertIn(response, context.response)
