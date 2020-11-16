from __future__ import absolute_import, unicode_literals
from django.db import connection
from datetime import datetime, timedelta, date
from .models import Schedule, ScheduleLog
import time
from signal import pause
from django.utils import timezone
import pytz

def start_schedule_time(pin):
	try:
		schedule = Schedule.objects.get(gpio_pin=pin)
		schedule_log = ScheduleLog()
		schedule_log.start = schedule.start
		schedule_log.deration=schedule.deration
		schedule_log.finish=schedule.finish
		schedule_log.finish_date = schedule.finish_date
		schedule_log.next_schedule = schedule.next_schedule
		schedule_log.start_date = schedule.start_date
		schedule_log.how_often = schedule.how_often
		schedule_log.run_time = schedule.run_time
		schedule_log.gpio_pin = schedule.gpio_pin
		schedule_log.save()
		start = datetime.combine(date.min, schedule.start) - datetime.min
		der = datetime.combine(date.min, schedule.deration) - datetime.min
		finish_time = start + der
		often = datetime.combine(date.min, schedule.how_often) - datetime.min
		next_time = finish_time + often
		get_difference = next_time - finish_time
		next_finish_time = next_time + get_difference

		# next_finish_time = next_finish_time - datetime.timedelta(seconds=60)
		# next_time = next_time - datetime.timedelta(seconds=60)

		today = datetime.today().strftime("%Y-%m-%d")
		next_finish_time= datetime.strptime(today+' '+str(next_finish_time), "%Y-%m-%d %H:%M:00")
		next_time= datetime.strptime(today+' '+str(next_time), "%Y-%m-%d %H:%M:00")
		schedule.finish = next_finish_time.strftime("%H:%M:00")
		schedule.finish_date=next_finish_time.strftime("%Y-%m-%d %H:%M:00")
		schedule.start = next_time.strftime("%H:%M:00")
		schedule.next_schedule=next_time.strftime("%Y-%m-%d %H:%M:00")
		schedule.save()
		return 'YEET'
	except Exception as e:
		print(e)
		return e

def next_schedule_time(pin):
	try:
		schedule = Schedule.objects.get(gpio_pin=pin)
		start = datetime.combine(date.min, schedule.start) - datetime.min
		der = datetime.combine(date.min, schedule.deration) - datetime.min
		finish_time = start + der
		often = datetime.combine(date.min, schedule.how_often) - datetime.min
		next_time = finish_time + often

		# finish_time = finish_time - datetime.timedelta(seconds=60)
		# next_time = next_time - datetime.timedelta(seconds=60)

		today = datetime.today().strftime("%Y-%m-%d")
		finish_time= datetime.strptime(today+' '+str(finish_time), "%Y-%m-%d %H:%M:00")
		next_time= datetime.strptime(today+' '+str(next_time), "%Y-%m-%d %H:%M:00")

		schedule.finish =finish_time.strftime("%H:%M:00")
		schedule.finish_date=finish_time.strftime("%Y-%m-%d %H:%M:00")
		schedule.next_schedule=next_time.strftime("%Y-%m-%d %H:%M:00")
		schedule.save()
		return 'YEET'
	except Exception as e:
		print(e)
		return e