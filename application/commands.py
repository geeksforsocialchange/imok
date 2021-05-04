from django.utils.translation import gettext as _
from django.conf import settings
from django.utils import timezone
from .contact_admins import notify_admins



def handle_command(message, member):
    command = message.split(' ')[0].upper()
    params = " ".join(message.split(' ')[1:])

    if command == 'YES' or command == 'Y' or command == '/START':
        return register(member)
    elif command == 'IN' or command == 'I':
        return checkin(member)
    elif command == 'NAME':
        return name(member, params)
    elif command == 'SOS' or command == 'HELP':
        return sos(member)
    elif command == 'O' or command == 'OUT':
        return checkout(member)
    elif command == "INFO":
        return info(member)
    else:
        return _("Sorry, I didn't understand that message.\n\nSend INFO for a list of commands I understand.")


def register(member):
    member.registered = True
    member.save()
    time = timezone.localtime().time()
    date = timezone.localtime().date()
    notify_admins("New Member",
                  f"{member.name} ({member.phone_number}) successfully activated their account at {time} on {date}.")
    return info(member)


def name(member, params):
    member.name = params
    member.save()
    response = _("You have set your name to %(name)s") % {'name': params}
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
    return _("Welcome to %(server)s, %(member name)s!\n\nYou can send me the following commands, "
             "or text %(imok phone number)s:\n\nIN: Check in to %(signing center)s\n\nOUT: Check out (after check "
             "in)\n\nNAME: Update your name\n\nSOS: Raise the alarm\n\nINFO: Get this message again" % {
                 "server": settings.SERVER_NAME,
                 "member name": member.name,
                 "imok phone number": settings.TWILIO_FROM_NUMBER,
                 "signing center": member.signing_center
             })
