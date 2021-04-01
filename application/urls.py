from django.urls import path

from . import views

urlpatterns = [
    path('twilio', views.twilio, ),
    path('telegram', views.telegram, )
]
