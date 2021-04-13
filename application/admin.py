from django.contrib import admin
from django.conf import settings
from django.utils.translation import gettext as _
import django.utils.timezone as timezone
from django.utils import translation
from .models import Checkin, Member


def send_invite(obj, user):
    obj.send_message(_("Welcome to imok! Your number has been added by %(admin)s. Would you like to register for this service? \n\nReply YES if so" % user))


class MemberAdmin(admin.ModelAdmin):
    fields = ('name', 'notes', 'language', 'registered', 'phone_number', 'telegram_username', 'signing_center', 'is_ok')
    search_fields = ['name', 'phone_number', 'telegram_username']
    list_display = ('phone_number', 'telegram_username', 'name', 'registered', 'is_ok')
    list_filter = ('is_ok', 'registered', 'language', 'signing_center')

    def save_model(self, request, obj, form, change):
        cur_language = translation.get_language()
        user_language = obj.language
        translation.activate(user_language)

        if obj.registered_by is None:
            obj.registered_by = request.user
            send_invite(obj, request.user)
        if 'is_ok' in form.changed_data:
            obj.send_message(_(f"An admin has marked you as {obj.ok_status()}"))
        translation.activate(cur_language)
        obj.save()


class CheckinAdmin(admin.ModelAdmin):
    list_display = ['checkin_user', 'checkin_phone_number', 'checkin_telegram_username', 'time_stamp', 'overdue', 'is_ok']
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
        return obj.time_stamp < timezone.now() - settings.CHECKIN_TTL

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
