from django.http import HttpResponse
from django.utils.translation import gettext as _


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
    else:
        return HttpResponse('Invalid Command')


def register(member):
    member.registered = True
    member.save()

    response = " ".join([_("Thanks for registering, %(name)s!") % {'name': member.name},
                _("To sign in, text IN or I to this number."),
                _("To correct your name, text NAME followed by your name."),
                _("To get emergency help, text SOS or HELP.")
                ])
    return response


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
