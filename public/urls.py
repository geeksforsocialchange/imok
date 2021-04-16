from django.urls import path


from . import views

app_name = 'public'
urlpatterns = [
    path('', views.index, name='index'),
    path('healthz', views.healthz, name='healthz'),
    path('varz', views.varz, name='varz'),
]
