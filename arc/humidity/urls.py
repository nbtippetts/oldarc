from django.urls import path
from django.shortcuts import render
from .views import humidity, set_humidity_temp, ajax_humidity, relay_on_off_17_18
# from .views import line_chart, line_chart_json

urlpatterns = [
    path('', humidity, name='humidity_view'),
    path('humidity_temperature', set_humidity_temp, name='humidity_temperature'),
    path('relay_on_off_17_18', relay_on_off_17_18, name='relay_on_off_17_18'),
    path('ajax_humidity', ajax_humidity, name='ajax_humidity'),
]
