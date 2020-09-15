from __future__ import absolute_import, unicode_literals
from celery import shared_task
from arc.celery import app
from django.db import connection
from datetime import datetime, timedelta, date
from .models import Schedule, WaterPump
from django_celery_beat.models import PeriodicTasks, PeriodicTask, IntervalSchedule
import time
import gpiozero
from gpiozero import LED, Button, Servo


@shared_task
def start_task(**kwargs):
	print(kwargs['pin'])
	if 'pin' in kwargs:
		schedule_obj = Schedule.objects.last()
		now_time = datetime.now().time()
		now_date = datetime.now()
		t = datetime.combine(date.min, schedule_obj.deration) - datetime.min
		while now_time > schedule_obj.start and now_time < schedule_obj.finish:
			try:
				relay = gpiozero.OutputDevice(kwargs['pin'], active_high=False, initial_value=False)
				relay.on()
				time.sleep(t.seconds)
			except gpiozero.exc.GPIOPinInUse as e:
				print(e)
				return
		else:
			relay = gpiozero.OutputDevice(kwargs['pin'], active_high=False, initial_value=False)
			relay.off()
	else:
		return "No GPIO in args."


@shared_task
def relay_task(status,pin):
	relay = gpiozero.OutputDevice(pin, active_high=False, initial_value=False)
	while status:
		relay.on()