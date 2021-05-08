import csv

from django.conf import settings
from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils import timezone
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

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
    readonly_fields = ('codename',)
    search_fields = ['codename', 'name', 'phone_number', 'telegram_username']
    list_display = ('codename', 'name', 'phone_number', 'telegram_username', 'registered', 'is_ok')
    list_filter = ('is_ok', 'registered', 'language', 'signing_center')

    def resend_invite(self, request, queryset):
        for member in queryset:
            if member.phone_number is None:
                messages.error(request, f"{member.name} has no phone number configured, couldn't send SMS")
            send_invite(member)
        print("sent invite")

    def save_model(self, request, obj, form, change):
        cur_language = translation.get_language()
        user_language = obj.language
        translation.activate(user_language)

        if obj.registered_by is None:
            if not settings.REQUIRE_INVITE:
                obj.registered = True
            obj.registered_by = request.user
            send_invite(obj)
            if obj.phone_number is None:
                messages.warning(request, "Couldn't send an sms invite because the member has no phone number. Either "
                                          "send them a link to the telegram bot or add a phone number and re-send the"
                                          " invite.  Suggested text:")
                messages.warning(request, mark_safe(_("You've been invited to join %(server name)s!<br/>"
                                                      "Would you like to register for this service?<br/>"
                                                      "If so, go to this link: %(signup_url)s<br/>"
                                                      "Then, send INFO to get a command list." % {
                                                          "server name": settings.SERVER_NAME,
                                                          "signup_url": bot_link()})))
        if 'is_ok' in form.changed_data:
            obj.send_message(_("An admin has marked you as %(status)s" % {'status': obj.ok_status()}))
        translation.activate(cur_language)
        obj.save()

    if settings.REQUIRE_INVITE:
        resend_invite.short_description = "Re-send SMS Invite"
        actions = ["resend_invite"]


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
