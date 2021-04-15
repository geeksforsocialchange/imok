from django.http import HttpResponse
from django.urls import path

from application.models import Member

def index(request):
    if Member.objects.count() == 0:
        return HttpResponse("Welcome to imok. You're probably looking for the <a href='/ruok'>admin screen.</a>")
    else:
        return HttpResponse("")
