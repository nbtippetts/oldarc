from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('', views.schedule, name='schedule'),
    path('relay/', views.relay_on_off,name='relay'),
    path('check_schedule/', views.check_schedule, name='check_schedule'),
]
