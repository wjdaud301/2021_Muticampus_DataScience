from django.urls import path
from . import views
from home.dash_apps.finished_apps import simpleexample, scatter, datatable


urlpatterns=[
    path('', views.home, name='home')
]