from behave import given, when, then

from application.models import Member, Checkin


@given(u'I have been registered as a member who speaks {language}')
def step_impl(context, language):
    member = Member(phone_number='+12025550483', name="Fake User", language=language)
    member.save()
    context.member = member
