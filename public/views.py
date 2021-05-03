from logging import getLogger
from django.http import HttpResponse
from application.models import Member

logger = getLogger('django')


def index(request):
    if Member.objects.count() == 0:
        return HttpResponse("Welcome to imok. You're probably looking for the <a href='/ruok'>admin screen.</a>")
    else:
        return HttpResponse("")


def healthz(request):
    if database_ok():
        return HttpResponse("OK")


def database_ok():
    try:
        from django.db import connections
    except ImportError as e:
        logger.exception(e)
        return False

    try:
        for name in connections:
            cursor = connections[name].cursor()
            cursor.execute("SELECT 1;")
            row = cursor.fetchone()
            if row is None:
                return False
    except Exception as e:
        logger.exception(e)
        return False
    else:
        return True
