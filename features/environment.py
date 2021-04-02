from django.conf import settings

settings.NOTIFY_EMAIL = 'root@localhost'
settings.DEBUG = True


def before_all(context):
    context.users = {}
    context.members = {}
