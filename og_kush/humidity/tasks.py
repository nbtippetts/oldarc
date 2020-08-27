from __future__ import absolute_import, unicode_literals
from django_celery_beat.models import PeriodicTasks, PeriodicTask, IntervalSchedule
from celery import shared_task
from og_kush.celery import app
from django.db import connection
from datetime import datetime, timedelta, date
from .models import HumidityTemp
import time
import Adafruit_DHT

@shared_task
def log_humidity_temp():
	sensor = Adafruit_DHT.DHT11
	pin = 2
	while True:
		hum, temperature = Adafruit_DHT.read_retry(sensor, pin)
		if hum is not None and temperature is not None:
			print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, hum))
			humidity_temp_db = HumidityTemp(
				humidity=hum,
				temp=temperature,
				created_at=datetime.now()
			)
			humidity_temp_db.save()
			return hum, temperature
		else:
			print("Failed to retrieve data from humidity sensor, Retry")
	return
