from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('', views.schedule, name='schedule'),
    path('update_schedule', views.update_schedule, name='update_schedule'),
]
