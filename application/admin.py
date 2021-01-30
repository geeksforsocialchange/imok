from django.contrib import admin

from .models import Subscriber, Invite, Checkin

admin.site.register(Subscriber)
admin.site.register(Invite)
admin.site.register(Checkin)
