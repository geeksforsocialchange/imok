from behave import given, when, then

from application.models import Member

@when(u'I request \'/\'')
def step_impl(context):
    # context.browser.get('http://localhost:8000/')
    raise NotImplementedError(u'STEP: When I request \'/\'')

@when(u'there are no members')
def step_impl(context):
    raise NotImplementedError(u'STEP: When there are no members')

@then(u'I see \'Welcome to imok\'')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I see \'Welcome to imok\'')

@when(u'there are members')
def step_impl(context):
    raise NotImplementedError(u'STEP: When there are members')


@then(u'I do not see \'Welcome to imok\'')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I do not see \'Welcome to imok\'')
