from __future__ import absolute_import, unicode_literals
from celery.task.control import revoke
from arc.celery import app
from celery.schedules import crontab
from django.db import connection
from celery.decorators import periodic_task
from datetime import datetime, timedelta, date
from .models import Schedule, Relay, Relay14, Relay15
import time
import gpiozero
from signal import pause
import redis
from signal import pause
from datetime import datetime
from django.utils import timezone
import pytz
from .set_schedule import start_schedule_time, next_schedule_time
app.control.purge()
rdb = redis.Redis(host='redis',port=6379,db=0)
# rdb = redis.Redis(host='redis',port=6379,db=0)

@periodic_task(
    run_every=crontab("*"),
    name="schedule.tasks.check_task_14"
)
def check_task_14():
	task = Relay14.objects.get(gpio_pin=14)
	task_schedule =  Schedule.objects.get(gpio_pin=14)
	get_now = datetime.now()
	get_now_time = datetime.now().time()
	print(get_now_time)
	if not rdb.exists('schedule_gpio_14'):
		rdb.set("schedule_gpio_14","OFF")
	relay_status = rdb.get("schedule_gpio_14")
	if get_now_time >=  task_schedule.start and get_now_time <= task_schedule.finish:
		if relay_status == b'ON':
			return 'Relay14 is on so exit'
		else:
			rdb.set("schedule_gpio_14","ON")
			check_relay = rdb.get("gpio_14")
			if check_relay == b'ON':
				relay_task_14.delay(False, 14)
				rdb.set("gpio_14","OFF")
				time.sleep(3)
			next_schedule_time(14)
			start_task_14.delay(True)
			return 'Turn Relay14 ON'

	if relay_status == b'ON':
		rdb.set("schedule_gpio_14","OFF")
		start_schedule_time(14)
		start_task_14.delay(False)
		return 'Turn Relay14 OFF'
	else:
		return " Relay14 already OFF so exit"

@app.task(bind=True,queue="queue_schedule_14",max_retry=0,ignore_results=True)
def start_task_14(self,status):
	relay = gpiozero.OutputDevice(14, active_high=False, initial_value=False)
	task = Relay14.objects.get(gpio_pin=14)
	if status:
		print(self.AsyncResult(self.request.id))
		task_id = self.AsyncResult(self.request.id)
		task.task_id = task_id
		task.relay_start = datetime.now()
		task.save()
		relay.on()
		print("relay14 is now ON")
		pause()
	else:
		task.relay_state = False
		task.relay_finish = datetime.now()
		print('Relay14 OFF')
		try:
			task_id = Relay14.objects.get(gpio_pin=14)
			revoke(task_id.task_id, terminate=True)
		except Exception as e:
			pass


@periodic_task(
    run_every=crontab("*"),
    name="schedule.tasks.check_task_15"
)
def check_task_15():
	task = Relay15.objects.get(gpio_pin=15)
	task_schedule =  Schedule.objects.get(gpio_pin=15)
	get_now = datetime.now()
	get_now_time = datetime.now().time()
	print(get_now_time)
	if not rdb.exists('schedule_gpio_15'):
		rdb.set("schedule_gpio_15","OFF")
	relay_status = rdb.get("schedule_gpio_15")
	if get_now_time >=  task_schedule.start and get_now_time <= task_schedule.finish:
		if relay_status == b'ON':
			return 'Relay15 is on so exit'
		else:
			rdb.set("schedule_gpio_15","ON")
			check_relay = rdb.get("gpio_15")
			if check_relay == b'ON':
				relay_task_15.delay(False, 15)
				rdb.set("gpio_15","OFF")
				time.sleep(3)
			next_schedule_time(15)
			start_task_15.delay(True)
			return 'Turn Relay15 ON'

	if relay_status == b'ON':
		rdb.set("schedule_gpio_15","OFF")
		start_schedule_time(15)
		start_task_15.delay(False)
		return 'Turn Relay15 OFF'
	else:
		return " Relay15 already OFF so exit"

@app.task(bind=True,queue="queue_schedule_15",max_retry=0,ignore_results=True)
def start_task_15(self, status):
	relay = gpiozero.OutputDevice(15, active_high=False, initial_value=False)
	task = Relay15.objects.get(gpio_pin=15)
	if status:
		print(self.AsyncResult(self.request.id))
		task_id = self.AsyncResult(self.request.id)
		task.task_id = task_id
		task.relay_start = datetime.now()
		task.save()
		relay.on()
		print("relay15 is now ON")
		pause()
	else:
		task.relay_state = False
		task.relay_finish = datetime.now()
		print('Relay15 OFF')
		try:
			task_id = Relay15.objects.get(gpio_pin=15)
			revoke(task_id.task_id, terminate=True)
		except Exception as e:
			pass

@app.task(bind=True,queue="queue_relay_14",max_retry=0,ignore_results=True)
def relay_task_14(self, status,pin):
	relay = gpiozero.OutputDevice(pin, active_high=False, initial_value=False)
	task = Relay.objects.get(gpio_pin=14)
	if status:
		print(self.AsyncResult(self.request.id))
		task_id = self.AsyncResult(self.request.id)
		task.relay_state = True
		task.task_id = task_id
		task.relay_start = datetime.now()
		task.gpio_pin = 14
		task.save()
		relay.on()
		print("relay is now ON")
		pause()
	else:
		task.relay_state = False
		task.relay_finish = datetime.now()
		relay.off()
		print('Relay OFF')
		try:
			task_id = Relay.objects.get(gpio_pin=14)
			revoke(task_id.task_id, terminate=True)
		except Exception as e:
			pass

@app.task(bind=True,queue="queue_relay_15",max_retry=0,ignore_results=True)
def relay_task_15(self, status,pin):
	relay = gpiozero.OutputDevice(pin, active_high=False, initial_value=False)
	task = Relay.objects.get(gpio_pin=15)
	if status:
		print(self.AsyncResult(self.request.id))
		task_id = self.AsyncResult(self.request.id)
		task.relay_state = True
		task.task_id = task_id
		task.relay_start = datetime.now()
		task.gpio_pin = 15
		task.save()
		relay.on()
		print("relay is now ON")
		pause()
	else:
		task.relay_state = False
		task.relay_finish = datetime.now()
		relay.off()
		print('Relay OFF')
		try:
			task_id = Relay.objects.get(gpio_pin=15)
			revoke(task_id.task_id, terminate=True)
		except Exception as e:
			pass