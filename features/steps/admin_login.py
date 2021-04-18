from behave import given, when, then

from application.models import Member, Checkin, MetricHour
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from django.contrib.admin.sites import AdminSite
from application.admin import MemberAdmin


class MockRequest(object):
    def __init__(self, user=None):
        self.user = user


@given(u'I have been registered as a staff user')
def step_impl(context):
    context.adminuser = User.objects.create_user(username='alice', password='password', is_staff=True)
    context.adminuser.save()


@when(u'I login')
def step_impl(context):
    context.test.client.login(username='alice', password='password')


@then(u'I can see {model}s')
def step_impl(context, model):
    response = context.test.client.get(f'/ruok/application/{model}/')
    context.test.assertEqual(response.status_code, 200)


@given(u'I have permission to view member')
def step_impl(context):
    content_type = ContentType.objects.get_for_model(Member)
    permission = Permission.objects.get(content_type=content_type, codename='view_member')
    context.adminuser.user_permissions.add(permission)


@given(u'I do not have permission to view member')
def step_impl(context):
    content_type = ContentType.objects.get_for_model(Member)
    permission = Permission.objects.get(content_type=content_type, codename='view_member')
    context.adminuser.user_permissions.remove(permission)


@given(u'I have permission to view checkin')
def step_impl(context):
    content_type = ContentType.objects.get_for_model(Checkin)
    permission = Permission.objects.get(content_type=content_type, codename='view_checkin')
    context.adminuser.user_permissions.add(permission)


@given(u'I do not have permission to view checkin')
def step_impl(context):
    content_type = ContentType.objects.get_for_model(Checkin)
    permission = Permission.objects.get(content_type=content_type, codename='view_checkin')
    context.adminuser.user_permissions.remove(permission)


@then(u'I can see {model}')
def step_impl(context, model):
    response = context.test.client.get(f'/ruok/application/{model}/')
    context.test.assertEqual(response.status_code, 200)


@then(u'I can not see {model}')
def step_impl(context, model):
    response = context.test.client.get(f'/ruok/application/{model}/')
    context.test.assertEqual(response.status_code, 403)


@given(u'I have been registered as a superuser')
def step_impl(context):
    context.superuser = User.objects.create_superuser(username='bob', password='password', is_staff=True)
    context.superuser.save()


@when(u'I create a read-only user')
def step_impl(context):
    context.test.assertTrue(context.superuser.is_superuser)
    context.adminuser = User.objects.create_user(username='alice', password='password', is_staff=True)

    content_type = ContentType.objects.get_for_model(Checkin)
    permission = Permission.objects.get(content_type=content_type, codename='view_checkin')
    context.adminuser.user_permissions.add(permission)

    content_type = ContentType.objects.get_for_model(Member)
    permission = Permission.objects.get(content_type=content_type, codename='view_member')
    context.adminuser.user_permissions.add(permission)

    context.adminuser.save()


@then(u'the user has permissions to view {model}s')
def step_impl(context, model):
    context.test.client.login(username='alice', password='password')
    response = context.test.client.get(f'/ruok/application/{model}/')
    context.test.assertEqual(response.status_code, 200)


@then(u'the user does not have permission to edit members')
def step_impl(context):
    from django.forms.models import model_to_dict

    context.test.client.login(username='alice', password='password')
    data = model_to_dict(Member())
    data['_save'] = 'save'
    data['registered_by'] = context.adminuser
    data['phone_number'] = ''
    data['is_ok'] = True
    response = context.test.client.post("/ruok/application/member/add/", data)
    context.test.assertEqual(response.status_code, 403)


@when(u'I create an admin user')
def step_impl(context):
    context.test.assertTrue(context.superuser.is_superuser)
    context.adminuser = User.objects.create_user(username='alice', password='password', is_staff=True)

    content_type = ContentType.objects.get_for_model(Checkin)
    permission = Permission.objects.get(content_type=content_type, codename='view_checkin')
    context.adminuser.user_permissions.add(permission)
    permission = Permission.objects.get(content_type=content_type, codename='delete_checkin')
    context.adminuser.user_permissions.add(permission)

    content_type = ContentType.objects.get_for_model(Member)
    permission = Permission.objects.get(content_type=content_type, codename='view_member')
    context.adminuser.user_permissions.add(permission)
    permission = Permission.objects.get(content_type=content_type, codename='change_member')
    context.adminuser.user_permissions.add(permission)
    permission = Permission.objects.get(content_type=content_type, codename='add_member')
    context.adminuser.user_permissions.add(permission)
    permission = Permission.objects.get(content_type=content_type, codename='delete_member')
    context.adminuser.user_permissions.add(permission)

    context.adminuser.save()


@then(u'the user has permission to edit members')
def step_impl(context):
    from django.forms.models import model_to_dict

    context.test.client.login(username='alice', password='password')
    data = model_to_dict(Member())
    data['_save'] = 'save'
    data['registered_by'] = context.adminuser
    data['phone_number'] = ''
    data['is_ok'] = True
    response = context.test.client.post("/ruok/application/member/add/", data)
    context.test.assertEqual(response.status_code, 200)


@given(u'I have permission to view metrichour')
def step_impl(context):
    content_type = ContentType.objects.get_for_model(MetricHour)
    permission = Permission.objects.get(content_type=content_type, codename='view_metrichour')
    context.adminuser.user_permissions.add(permission)


@given(u'I do not have permission to view metrichour')
def step_impl(context):
    content_type = ContentType.objects.get_for_model(MetricHour)
    permission = Permission.objects.get(content_type=content_type, codename='view_metrichour')
    context.adminuser.user_permissions.remove(permission)
