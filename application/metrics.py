import uuid
from django.db import models, transaction
from django.utils import timezone


class MetricHour(models.Model):
    id = models.fields.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    metric = models.CharField(max_length=60, db_index=True)
    value = models.CharField(max_length=50, db_index=True)
    num = models.IntegerField('count', default=0)
    date = models.DateField()
    hour = models.IntegerField(default=-1)

    class Meta:
        verbose_name = "Hourly metric"
        verbose_name_plural = "Hourly metrics"


def increment_hourly_metric(metric, value):
    now = timezone.localtime()
    with transaction.atomic():
        metric, created = MetricHour.objects.get_or_create(metric=metric, value=value, date=now.date(), hour=now.hour)
        metric = MetricHour.objects.select_for_update().get(id=metric.id)
        metric.num = metric.num + 1
        metric.save()
