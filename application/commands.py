from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _

from .contact_admins import notify_admins
from .telegram_botinfo import bot_link
import logging

logger = logging.getLogger(__name__)


def handle_command(message, member):
    command = message.split(' ')[0].upper()
    params = " ".join(message.split(' ')[1:])

    if command == 'YES' or command == 'Y' or command == '/START':
        return register(member)
    elif command == 'IN' or command == 'I':
        return checkin(member)
    elif command == 'NAME':
        return name(member, params)
    elif command == 'SOS':
        return sos(member)
    elif command == 'O' or command == 'OUT':
        return checkout(member)
    elif command == "INFO":
        return info(member)
    else:
        return _("Sorry, I didn't understand that message.\n\nSend INFO for a list of commands I understand.")


def register(member):
    if not member.registered:
        member.registered = True
        member.save()
        time = timezone.localtime().strftime('%X')
        date = timezone.localtime().strftime('%x')
        try:
            notify_admins(f"🎉 {member.name} activated their account!",
                          f"🎉 {member.name} ({member.phone_number}) successfully activated their account at {time} on {date}!")
        except:
            logger.warning("Failed to notify admins of a new member")
    return info(member)


def name(member, params):
    if len(params) > 0:
        member.name = params
        member.save()
        response = _("You have set your name to %(name)s") % {'name': params}
        return response
    else:
        response = _("To change your name, send NAME followed by your name")
        response = response + "\n"
        # Translators: you can generate a random name for a suitable region using https://www.behindthename.com/random/
        response = response + _("For example: 'NAME  Jabir Reem'")
        return response


def checkin(member):
    response = member.sign_in()
    return response


def checkout(member):
    response = member.sign_out()
    return response


def sos(member):
    response = member.handle_sos()
    return response


def info(member):
    return _("Welcome to %(server)s, %(member name)s!\n\n"
             "You can send me the following commands, or text %(imok phone number)s:\n\n"
             "IN: Check in to %(signing center)s\n\n"
             "OUT: Check out (after check in)\n\n"
             "NAME: Update your name\n\n"
             "SOS: Raise the alarm\n\n"
             "INFO: Get this message again\n\n"
             "You can also message me on Telegram: %(telegram link)s") % {
                 "server": settings.SERVER_NAME,
                 "member name": member.name,
                 "imok phone number": settings.TWILIO_FROM_NUMBER,
                 "signing center": member.signing_center,
                 "telegram link": bot_link()
             }
