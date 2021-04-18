from behave import then
from application.models import MetricHour
from django.db.models import Sum


@then(u'There is 1 checkin')
def step_impl(context):
    total = MetricHour.objects.filter(metric='checkin').aggregate(Sum('num'))['num__sum']
    context.test.assertEqual(total, 1)


@then(u'There are {number} checkins')
def step_impl(context, number):
    total = MetricHour.objects.filter(metric='checkin').aggregate(Sum('num'))['num__sum']
    context.test.assertEqual(total, int(number))
