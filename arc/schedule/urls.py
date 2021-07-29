from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('', views.schedule, name='schedule'),
    path('update_schedule', views.update_schedule, name='update_schedule'),
    path('relay_on_off', views.relay_on_off, name='relay_on_off'),
]
