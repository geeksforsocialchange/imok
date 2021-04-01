from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('twilio', views.twilio, ),
    path('telegram', views.telegram, )
]
