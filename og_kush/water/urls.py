from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('', views.water, name='og-water'),
    path('water_pump/', views.start_pump, name='pump'),
    path('check_water/', views.check_water, name='check_water'),
]
