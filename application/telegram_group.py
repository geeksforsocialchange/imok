from django.db import models


class TelegramGroup(models.Model):
    title = models.CharField(max_length=255, unique=True, primary_key=True)
    chat_id = models.BigIntegerField(default=0, unique=True)
