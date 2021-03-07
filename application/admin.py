from django.contrib import admin
from imok.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER
from twilio.rest import Client
from django.utils.translation import gettext as _

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
        # @TODO send acknowledgement on changing is_ok
        if obj.registered_by is None:
            obj.registered_by = request.user
            send_invite(obj)
        obj.save()


admin.site.register(Member, MemberAdmin)
