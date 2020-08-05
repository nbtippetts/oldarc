from django.urls import path
from django.shortcuts import render
from . import views

urlpatterns = [
    path('', views.water, name='og-water'),
    path('check-water/', views.check_water, name='og-check-water'),
]
