from __future__ import absolute_import, unicode_literals
from celery.task.control import revoke
from arc.celery import app
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
app.control.purge()
rdb = redis.Redis(host='localhost',port=6379,db=0)
# rdb = redis.Redis(host='localhost',port=6379,db=0)

@periodic_task(
    run_every=10,
    name="schedule.tasks.check_task_14"
)
def check_task_14():
	try:
		task = Relay14.objects.get(gpio_pin=14)
	except Exception as e:
		print('no data')
		r = Relay14(
			relay_state=False,
			task_id='False',
			gpio_pin=14,
		)
		r.save()
		task = Relay14.objects.get(gpio_pin=14)
	task_schedule =  Schedule.objects.get(gpio_pin=14)
	get_now = timezone.now()
	get_now_time = timezone.now().time()
	if get_now > task_schedule.start_date:
		if get_now > task_schedule.next_schedule:
			if get_now_time >  task_schedule.start and get_now_time < task_schedule.finish:
				if task.relay_state:
					return 'Relay14 is on so exit'
				else:
					start_task_14.delay(True)
					return 'Turn Relay14 ON'
			else:
				ws = datetime.combine(
					date.min, task_schedule.start) - datetime.min
				t = datetime.today()
				d = datetime.combine(t,task_schedule.deration)
				finish_time = ws + d
				nw = datetime.combine(
					date.min, task_schedule.how_often) - datetime.min
				next_time = finish_time + nw
				schedule = Schedule.objects.get(gpio_pin=14)
				full_date = datetime.combine(task_schedule.start_date,task_schedule.start)
				schedule.start_date=full_date.strftime("%Y-%m-%d %H:%M:%S")
				print(schedule.start_date)
				schedule.start =str(task_schedule.start)
				print(schedule.start)
				schedule.how_often =str(task_schedule.how_often)
				print(schedule.how_often)
				schedule.deration =str(task_schedule.deration)
				print(schedule.deration)
				schedule.finish =finish_time.strftime("%H:%M:%S")
				# print(finish_time)
				print(schedule.finish)
				schedule.next_schedule=next_time.strftime("%Y-%m-%d %H:%M:%S")
				# print(next_time)
				print(schedule.next_schedule)
				schedule.finish_date=finish_time.strftime("%Y-%m-%d %H:%M:%S")
				print(schedule.finish_date)
				schedule.save()
				start_task_14.delay(False)
				return 'Turn Relay14 OFF'
		else:
			return 'Next Schedule Not Yet'
	else:
		return 'Start date no ready'

@app.task(bind=True,queue="queue_schedule",max_retry=0,ignore_results=True)
def start_task_14(self,status):
	relay = gpiozero.OutputDevice(14, active_high=False, initial_value=False)
	try:
		task = Relay14.objects.get(gpio_pin=14)
	except Exception as e:
		print('no data')
		r = Relay(
			relay_state=False,
			task_id='False',
			gpio_pin=14,
		)
		r.save()
		task = Relay14.objects.get(gpio_pin=14)
	if status:
		print(self.AsyncResult(self.request.id))
		task_id = self.AsyncResult(self.request.id)
		task.relay_state = True
		task.task_id = task_id
		task.relay_start = timezone.now()
		task.gpio_pin = 14
		task.save()
		relay.on()
		rdb.set("gpio_14","ON")
		print("relay is now ON")
		pause()
	else:
		task.relay_state = False
		task.relay_finish = timezone.now()
		relay.off()
		rdb.set("gpio_14","OFF")
		print('Relay OFF')
		try:
			task_id = Relay14.objects.get(gpio_pin=14)
			revoke(task_id.task_id, terminate=True)
		except Exception as e:
			pass

@periodic_task(
    run_every=15,
    name="schedule.tasks.check_task_15"
)
def check_task_15():
	try:
		task = Relay15.objects.get(gpio_pin=15)
	except Exception as e:
		print('no data')
		r = Relay15(
			relay_state=False,
			task_id='False',
			gpio_pin=15,
		)
		r.save()
		task = Relay15.objects.get(gpio_pin=15)
	task_schedule =  Schedule.objects.get(gpio_pin=15)
	get_now = timezone.now()
	get_now_time = timezone.now().time()
	if get_now > task_schedule.start_date:
		if get_now > task_schedule.next_schedule:
			if get_now_time >  task_schedule.start and get_now_time < task_schedule.finish:
				if task.relay_state:
					return 'Relay15 is on so exit'
				else:
					start_task_15.delay(True)
					return 'Turn Relay15 ON'
			else:
				ws = datetime.combine(
					date.min, task_schedule.start) - datetime.min
				t = datetime.today()
				d = datetime.combine(t,task_schedule.deration)
				finish_time = ws + d
				nw = datetime.combine(
					date.min, task_schedule.how_often) - datetime.min
				next_time = finish_time + nw
				schedule = Schedule.objects.get(gpio_pin=15)
				full_date = datetime.combine(task_schedule.start_date,task_schedule.start)
				schedule.start_date=full_date.strftime("%Y-%m-%d %H:%M:%S")
				print(schedule.start_date)
				schedule.start =str(task_schedule.start)
				print(schedule.start)
				schedule.how_often =str(task_schedule.how_often)
				print(schedule.how_often)
				schedule.deration =str(task_schedule.deration)
				print(schedule.deration)
				schedule.finish =finish_time.strftime("%H:%M:%S")
				# print(finish_time)
				print(schedule.finish)
				schedule.next_schedule=next_time.strftime("%Y-%m-%d %H:%M:%S")
				# print(next_time)
				print(schedule.next_schedule)
				schedule.finish_date=finish_time.strftime("%Y-%m-%d %H:%M:%S")
				print(schedule.finish_date)
				schedule.save()
				start_task_15.delay(False)
				return 'Turn Relay15 OFF'
		else:
			return 'Next Schedule Not Yet'
	else:
		return 'Start date no ready'

@app.task(bind=True,queue="queue_schedule",max_retry=0,ignore_results=True)
def start_task_15(self,status):
	relay = gpiozero.OutputDevice(15, active_high=False, initial_value=False)
	try:
		task = Relay.objects.get(gpio_pin=15)
	except Exception as e:
		print('no data')
		r = Relay(
			relay_state=False,
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
		task.relay_start = timezone.now()
		task.gpio_pin = 15
		task.save()
		relay.on()
		rdb.set("gpio_15","ON")
		print("relay is now ON")
		pause()
	else:
		task.relay_state = False
		task.relay_finish = timezone.now()
		relay.off()
		rdb.set("gpio_15","OFF")
		print('Relay OFF')
		try:
			task_id = Relay.objects.get(gpio_pin=15)
			revoke(task_id.task_id, terminate=True)
		except Exception as e:
			pass


@app.task(bind=True,queue="queue_schedule",max_retry=0,ignore_results=True)
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
		task.relay_start = timezone.now()
		task.gpio_pin = 14
		task.save()
		relay.on()
		print("relay is now ON")
		pause()
	else:
		task.relay_state = False
		task.relay_finish = timezone.now()
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
		task.relay_start = timezone.now()
		task.gpio_pin = 15
		task.save()
		relay.on()
		print("relay is now ON")
		pause()
	else:
		task.relay_state = False
		task.relay_finish = timezone.now()
		relay.off()
		print('Relay OFF')
		try:
			task_id = Relay.objects.get(gpio_pin=15)
			revoke(task_id.task_id, terminate=True)
		except Exception as e:
			pass