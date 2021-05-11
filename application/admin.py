import csv

from django.conf import settings
from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils import timezone
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from .contact_admins import notify_admins
from .models import Checkin, Member, MetricHour
from .twilio import twilio_send
from .telegram_botinfo import bot_link


def send_invite(obj):
    if obj.phone_number is not None:
        message = _("You've been invited to join %(server name)s!\n\nWould you like to register for this "
                    "service?\n\nReply YES to join." % {'server name': settings.SERVER_NAME})
        twilio_send(obj.phone_number.as_e164, message)
        return message


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class MemberAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Member', {
            'fields': ('codename', 'name', 'notes', 'language', 'signing_center'),
            'description': ""
        }),
        ('Contact Details', {
            'fields': ('phone_number', 'telegram_username', 'preferred_channel')
        })
    )
    readonly_fields = ('codename', 'warning_message_sent_at', 'overdue_message_sent_at', 'sos_alert_received_at')
    search_fields = ['codename', 'name', 'phone_number', 'telegram_username']
    list_display = ('codename', 'name', 'phone_number', 'telegram_username', 'registered', 'is_ok', 'warning_message_sent_at', 'overdue_message_sent_at', 'sos_alert_received_at')
    list_filter = ('is_ok', 'registered', 'language', 'signing_center')
    actions = ["mark_ok", "resend_invite", "delete_checkin"]

    @admin.action(description="Resend SMS invite to selected members")
    def resend_invite(self, request, queryset):
        for member in queryset:
            if member.phone_number is None:
                messages.error(request, f"{member.name} has no phone number configured, so I couldn't an send SMS")
            send_invite(member)
        print("sent invite")

    @admin.action(description="Mark selected members as ok")
    def mark_ok(self, request, queryset):
        for member in queryset:
            member.is_ok = True
            member.warning_message_sent_at = None
            member.overdue_message_sent_at = None
            member.sos_alert_received_at = None
            member.save()
            msg = f"✅ {member.name} was marked safe by {request.user}"
            notify_admins(msg, msg)
            messages.success(request, f"Marked {member.name} as OK")

    @admin.action(description="Delete member's checkin")
    def delete_checkin(self, request, queryset):
        for member in queryset:
            try:
                member.checkin.delete()
            except Checkin.DoesNotExist:
                pass
        messages.success(request, "Deleted checkins for selected members")

    def save_model(self, request, obj, form, change):
        if obj.registered_by is None:
            if not settings.REQUIRE_INVITE:
                obj.registered = True
            obj.registered_by = request.user
            obj.save()
            with translation.override(obj.language, deactivate=True):
                send_invite(obj)
                if obj.phone_number is None:
                    messages.warning(request, "I couldn't invite this person by SMS because they have no phone number stored."
                                              "You can add a phone number and try again, or manually send them a Telegram invite.")
                    messages.info(request, mark_safe("<strong>Suggested Telegram invite message:</strong><br><br>"
                                                     "You've been invited to join %(server name)s!<br>"
                                                     "Would you like to register for this service?<br>"
                                                     "If so, go to this link: %(signup_url)s<br>"
                                                     "Then, send INFO to get a command list." % {
                                                          "server name": settings.SERVER_NAME,
                                                          "signup_url": bot_link()}))
        obj.save()


class CheckinAdmin(admin.ModelAdmin):
    list_display = ['checkin_user', 'checkin_phone_number', 'checkin_telegram_username', 'time_stamp', 'overdue',
                    'is_ok']
    list_filter = ['member__is_ok']
    list_select_related = True
    search_fields = ['member__name', 'member__phone_number', 'member__telegram_username']
    empty_value_display = 'unknown'
    list_display_links = None
    ordering = ['time_stamp']

    def checkin_user(self, obj):
        return f"{obj.member.name}"

    def checkin_phone_number(self, obj):
        return obj.member.phone_number

    def checkin_telegram_username(self, obj):
        return obj.member.telegram_username

    def overdue(self, obj):
        return obj.time_stamp < timezone.localtime() - settings.CHECKIN_TTL

    def is_ok(self, obj):
        return obj.member.is_ok

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    overdue.boolean = True
    is_ok.boolean = True


class MetricAdmin(admin.ModelAdmin, ExportCsvMixin):
    list_display = ['metric', 'value', 'num', 'date', 'hour']
    list_filter = ['metric', 'value']
    list_display_links = None
    actions = ["export_as_csv"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Member, MemberAdmin)
admin.site.register(Checkin, CheckinAdmin)
admin.site.register(MetricHour, MetricAdmin)
