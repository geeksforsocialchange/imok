from behave import given, when, then

from application.models import Member

@when(u'I request \'/\'')
def step_impl(context):
    context.response = context.test.client.get('/')

@when(u'there are no members')
def step_impl(context):
    Member.objects.all().delete()

@then(u'I see \'Welcome to imok\'')
def step_impl(context):
    context.test.assertIn('Welcome to imok', str(context.response.content, 'utf-8'))

@when(u'there are members')
def step_impl(context):
    Member.objects.create(name='Test user')

@then(u'I do not see \'Welcome to imok\'')
def step_impl(context):
    context.test.assertNotIn('Welcome to imok', str(context.response.content, 'utf-8'))
