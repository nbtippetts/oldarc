from __future__ import absolute_import, unicode_literals
from celery.task.control import revoke
from arc.celery import app
from django.db import connection
from celery.decorators import periodic_task
from datetime import datetime, timedelta, date
from .models import Schedule, Relay
import time
import gpiozero
from signal import pause
import redis
from signal import pause
app.control.purge()
# rdb = redis.Redis(host='redis',port=6379,db=0)
rdb = redis.Redis(host='localhost',port=6379,db=0)

def run_every_schedule_14():
	s = Schedule.objects.get(gpio_pin=14)
	t = datetime.combine(date.min, s.how_often) - datetime.min
	print(t.total_seconds())
	return t.total_seconds()

def run_every_schedule_15():
	s = Schedule.objects.get(gpio_pin=15)
	t = datetime.combine(date.min, s.how_often) - datetime.min
	print(t.total_seconds())
	return t.total_seconds()

@periodic_task(
    run_every=run_every_schedule_14(),
    name="schedule.start_task_14",
    queue="queue_schedule",
    options={"queue": "queue_schedule"},
)
def start_task_14(self):
	schedule_obj = Schedule.objects.last()
	now_time = datetime.now().time()
	now_date = datetime.now()
	t = datetime.combine(date.min, schedule_obj.deration) - datetime.min
	while now_time > schedule_obj.start and now_time < schedule_obj.finish:
		try:
			relay = gpiozero.OutputDevice(14, active_high=False, initial_value=False)
			relay.on()
			rdb.set("gpio_14","ON")
			time.sleep(t.seconds)
		except gpiozero.exc.GPIOPinInUse as e:
			print(e)
			return
	else:
		relay = gpiozero.OutputDevice(14, active_high=False, initial_value=False)
		relay.off()
		rdb.set("gpio_14","OFF")


@periodic_task(
    run_every=run_every_schedule_15(),
    name="schedule.start_task_15",
    queue="queue_schedule",
    options={"queue": "queue_schedule"},
)
def start_task_15(self):
	schedule_obj = Schedule.objects.last()
	now_time = datetime.now().time()
	now_date = datetime.now()
	t = datetime.combine(date.min, schedule_obj.deration) - datetime.min
	while now_time > schedule_obj.start and now_time < schedule_obj.finish:
		try:
			relay = gpiozero.OutputDevice(15, active_high=False, initial_value=False)
			relay.on()
			rdb.set("gpio_15","ON")
			time.sleep(t.seconds)
		except gpiozero.exc.GPIOPinInUse as e:
			print(e)
			return
	else:
		relay = gpiozero.OutputDevice(15, active_high=False, initial_value=False)
		relay.off()
		rdb.set("gpio_15","OFF")

@app.task(bind=True,queue="queue_schedule_14",max_retry=0,ignore_results=True)
def relay_task_14(self, status,pin):
	relay = gpiozero.OutputDevice(pin, active_high=False, initial_value=False)
	try:
		task = Relay.objects.get(gpio_pin=14)
	except Exception as e:
		print('no data')
		r = Relay(
			relay_state=status,
			task_id='False',
			gpio_pin=14,
		)
		r.save()
		task = Relay.objects.get(gpio_pin=14)
	if status:
		print(self.AsyncResult(self.request.id))
		task_id = self.AsyncResult(self.request.id)
		task.relay_state = True
		task.task_id = task_id
		task.gpio_pin = 14
		task.save()
		relay.on()
		print("relay is now ON")
		pause()
	else:
		task.relay_state = False
		relay.off()
		print('Relay OFF')
		try:
			task_id = Relay.objects.get(gpio_pin=14)
			revoke(task_id.task_id, terminate=True)
		except Exception as e:
			pass

@app.task(bind=True,queue="queue_schedule_15",max_retry=0,ignore_results=True)
def relay_task_15(self, status,pin):
	relay = gpiozero.OutputDevice(pin, active_high=False, initial_value=False)
	try:
		task = Relay.objects.get(gpio_pin=15)
	except Exception as e:
		print('no data')
		r = Relay(
			relay_state=status,
			task_id='False',
			gpio_pin=15,
		)
		r.save()
		task = Relay.objects.get(gpio_pin=15)
	if status:
		print(self.AsyncResult(self.request.id))
		task_id = self.AsyncResult(self.request.id)
		task.relay_state = True
		task.task_id = task_id
		task.gpio_pin = 15
		task.save()
		relay.on()
		print("relay is now ON")
		pause()
	else:
		task.relay_state = False
		relay.off()
		print('Relay OFF')
		try:
			task_id = Relay.objects.get(gpio_pin=15)
			revoke(task_id.task_id, terminate=True)
		except Exception as e:
			pass