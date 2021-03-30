from django.contrib import admin
from imok.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, CHECKIN_TTL
from twilio.rest import Client
from django.utils.translation import gettext as _
import django.utils.timezone as timezone

from .models import Checkin, Member


def send_invite(obj):
    print(f"Sending an invite to {obj.phone_number.as_e164}")
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        to=obj.phone_number.as_e164,
        from_=TWILIO_FROM_NUMBER,
        body=_("Welcome to imok! Your number has been added by %(admin)s. Would you like to register for this service? \n\nReply YES if so") % {'admin': obj.registered_by.username}
    )
    print(message.sid)


class MemberAdmin(admin.ModelAdmin):
    fields = ('name', 'notes', 'language', 'registered', 'phone_number', 'signing_center', 'is_ok')
    search_fields = ['name', 'phone_number']
    list_display = ('phone_number', 'name', 'registered', 'is_ok')
    list_filter = ('is_ok', 'registered', 'language', 'signing_center')

    def save_model(self, request, obj, form, change):
        if obj.registered_by is None:
            obj.registered_by = request.user
            send_invite(obj)
        if 'is_ok' in form.changed_data:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=_(f"An admin has marked you as {self.ok_status}"),
                from_=TWILIO_FROM_NUMBER,
                to=self.phone_number.as_e164
            )
            print(message.sid)
        obj.save()


class CheckinAdmin(admin.ModelAdmin):
    list_display = ['checkin_user', 'checkin_phone_number', 'time_stamp', 'overdue', 'is_ok']
    list_filter = ['member__is_ok']
    list_select_related = True
    search_fields = ['member__name', 'member__phone_number']
    empty_value_display = 'unknown'
    list_display_links = None
    ordering = ['time_stamp']

    def checkin_user(self, obj):
        return f"{obj.member.name}"

    def checkin_phone_number(self, obj):
        return obj.member.phone_number

    def overdue(self, obj):
        return obj.time_stamp < timezone.now() - CHECKIN_TTL

    def is_ok(self, obj):
        return obj.member.is_ok

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    overdue.boolean = True
    is_ok.boolean = True


admin.site.register(Member, MemberAdmin)
admin.site.register(Checkin, CheckinAdmin)
