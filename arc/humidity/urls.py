from django.urls import path
from django.shortcuts import render
from .views import humidity, set_humidity_temp, ajax_humidity
# from .views import line_chart, line_chart_json

urlpatterns = [
    path('', humidity, name='humidity_view'),
    path('humidity_temperature', set_humidity_temp, name='humidity_temperature'),
    path('ajax_humidity_url', ajax_humidity, name='ajax_humidity'),
]
