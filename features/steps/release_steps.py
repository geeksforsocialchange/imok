from behave import given, when, then
from application.management.commands.release import commit_message


@given(u'git rev {rev}')
def step_impl(context, rev):
    context.deployMessage = commit_message(rev)


@then(u'the deployment message contains {text}')
def step_impl(context, text):
    context.test.assertIn(text, context.deployMessage)
