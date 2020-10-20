from __future__ import absolute_import, unicode_literals
from celery import shared_task
from arc.celery import app
from django.db import connection
from datetime import datetime, timedelta, date
from .models import Schedule, WaterPump
import time
import gpiozero
from signal import pause
import redis
from signal import pause
app.control.purge()
rdb = redis.Redis(host='redis',port=6379,db=0)
#rdb = redis.Redis(host='localhost',port=6379,db=0)
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


@app.task(bind=True,max_retry=1, ignore_results=True, soft_time_limit=90000)
def relay_task(self, status,pin):
	if status and pin == '18':
		rdb.set("relay_key","ON")
	if not status and pin == '18':
		rdb.set("relay_key","OFF")
	relay = gpiozero.OutputDevice(pin, active_high=False, initial_value=False)
	if status:
		relay.on()
		pause()
	else:
		relay.off()
