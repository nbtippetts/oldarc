from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('', views.schedule, name='schedule'),
    path('water_pump/', views.start_pump, name='pump'),
    path('check_schedule/', views.check_schedule, name='check_schedule'),
]
