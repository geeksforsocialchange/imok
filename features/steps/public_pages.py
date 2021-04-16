from behave import when, then

from application.models import Member


@when(u'I request \'{page}\'')
def step_impl(context, page):
    context.response = context.test.client.get(page)


@when(u'there are no members')
def step_impl(context):
    Member.objects.all().delete()


@then(u'I see \'{content}\'')
def step_impl(context, content):
    context.test.assertIn(content, str(context.response.content, 'utf-8'))


@when(u'there are members')
def step_impl(context):
    Member.objects.create(name='Test user')


@then(u'I do not see \'{content}\'')
def step_impl(context, content):
    context.test.assertNotIn(content, str(context.response.content, 'utf-8'))
