from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('', views.schedule, name='schedule'),
    path('relay_on_off_14', views.relay_on_off_14,name='relay_on_off_14'),
    path('relay_on_off_15', views.relay_on_off_15,name='relay_on_off_15'),
    path('check_schedule/', views.check_schedule, name='check_schedule'),
]
