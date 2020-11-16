from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from datetime import datetime, timedelta, time, date
from django_celery_beat.models import PeriodicTasks, PeriodicTask, IntervalSchedule
from .models import Schedule, Relay, Relay14, Relay15
from .forms import ScheduleForm, RelayForm, RelayForm14, RelayForm15
import time
import json
from .tasks import relay_task_14, relay_task_15, start_task_14, start_task_15
import redis
from django.utils import timezone
import pytz
from .set_schedule import start_schedule_time, next_schedule_time

rdb = redis.Redis(host='redis',port=6379,db=0)
# rdb = redis.Redis(host='redis',port=6379,db=0)


def schedule(request):
	schedule_obj = Schedule.objects.all().order_by('-finish')[:3]
	context = {
		'waters': schedule_obj,
	}
	return redirect('/', context)

def relay_on_off_14(request):
	if not rdb.exists('gpio_14'):
		rdb.set("gpio_14","OFF")
	wat = Schedule.objects.all().order_by('-finish')[:3]
	if request.method == 'POST':
		relay_form = RelayForm(request.POST)
		if relay_form.is_valid():
			stat = False
			if relay_form.cleaned_data['relay_status'] == 'True':
				rdb.set("gpio_14","ON")
				try:
					relay14 = Relay.objects.get(gpio_pin=14)
				except Exception as e:
					print('no data')
					r = Relay(
						relay_state=relay_form.cleaned_data['relay_status'],
						relay_start = datetime.now(),
						relay_finish=datetime.now(),
						task_id='False',
						gpio_pin=14,
					)
					r.save()
					relay14 = Relay.objects.get(gpio_pin=14)
				relay14.relay_status=relay_form.cleaned_data['relay_status']
				relay14.relay_start = datetime.now()
				relay14.relay_finish=datetime.now()
				relay14.gpio_pin=14
				
				relay14.save()
				relay_task_14.delay(True, 14)
			if relay_form.cleaned_data['relay_status'] == 'False':
				rdb.set("gpio_14","OFF")
				try:
					relay14 = Relay.objects.get(gpio_pin=14)
					relay14.relay_status = relay_form.cleaned_data['relay_status']
					relay14.relay_finish = datetime.now()
					relay14.save()
					relay_status = rdb.get("schedule_gpio_14")
					if relay_status == b'ON':
						start_schedule_time(14)
						rdb.set("schedule_gpio_14","OFF")
						start_task_14.delay(False)
						relay_task_14.delay(False, 14)
					else:
						relay_task_14.delay(False, 14)
				except Exception as e:
					pass

			context = {
				'waters': wat,
				'form': relay_form
			}
			return redirect('/', context)
	else:
		form = RelayForm()
		context = {
			'waters': wat,
			'form': form
		}
		return redirect('/', context)

def relay_on_off_15(request):
	if not rdb.exists('gpio_15'):
		rdb.set("gpio_15","OFF")
	wat = Schedule.objects.all().order_by('-finish')[:3]
	if request.method == 'POST':
		relay_form = RelayForm(request.POST)
		if relay_form.is_valid():
			stat = False
			if relay_form.cleaned_data['relay_status'] == 'True':
				rdb.set("gpio_15","ON")
				try:
					relay15 = Relay.objects.get(gpio_pin=15)
				except Exception as e:
					print('no data')
					r = Relay(
						relay_state=relay_form.cleaned_data['relay_status'],
						relay_start = datetime.now(),
						relay_finish=datetime.now(),
						task_id='False',
						gpio_pin=15,
					)
					r.save()
					relay15 = Relay.objects.get(gpio_pin=15)
				relay15.relay_status=relay_form.cleaned_data['relay_status']
				relay15.relay_start = datetime.now()
				relay15.relay_finish=datetime.now()
				relay15.gpio_pin=15
				relay15.save()
				relay_task_15.delay(True, 15)
			if relay_form.cleaned_data['relay_status'] == 'False':
				rdb.set("gpio_15","OFF")
				try:
					relay15 = Relay.objects.get(gpio_pin=15)
					relay15.relay_status = relay_form.cleaned_data['relay_status']
					relay15.relay_finish = datetime.now()
					relay15.save()
					relay_status = rdb.get("schedule_gpio_15")
					if relay_status == b'ON':
						start_schedule_time(15)
						rdb.set("schedule_gpio_15","OFF")
						start_task_15.delay(False)
						relay_task_15.delay(False, 15)
					else:
						relay_task_15.delay(False, 15)
				except Exception as e:
					pass

			context = {
				'waters': wat,
				'form': relay_form
			}
			return redirect('/', context)
	else:
		form = RelayForm()
		context = {
			'waters': wat,
			'form': form
		}
		return redirect('/', context)


def update_schedule(request):
	# If this is a POST request then process the Form data
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request (binding):
		form = ScheduleForm(request.POST)
		# Check if the form is valid:
		if form.is_valid():
			get_hour = form.cleaned_data['how_often'].split(':')
			ws = datetime.combine(
				date.min, form.cleaned_data['start']) - datetime.min
			t = datetime.today()
			format_duration = t.strftime(
				'%Y-%m-%d')+' '+form.cleaned_data['deration']
			wd = datetime.strptime(
				format_duration, '%Y-%m-%d %H:%M:00')
			finish_time = ws + wd
			often = datetime.strptime(
				form.cleaned_data['how_often'], '%H:%M:00')
			nw = datetime.combine(
				date.min, often.time()) - datetime.min
			next_time = finish_time + nw
			schedule = Schedule.objects.get(gpio_pin=form.cleaned_data['gpio_pin'])
			full_date = datetime.combine(form.cleaned_data['start_date'],form.cleaned_data['start'])
			schedule.start_date=full_date.strftime("%Y-%m-%d %H:%M:00")
			print(schedule.start_date)
			schedule.start =form.cleaned_data['start'].strftime("%H:%M:00")
			print(schedule.start)
			schedule.how_often =often.strftime("%H:%M:00")
			print(schedule.how_often)
			schedule.deration =wd.strftime("%H:%M:00")
			print(schedule.deration)
			schedule.finish =finish_time.strftime("%H:%M:00")
			# print(finish_time)
			print(schedule.finish)
			schedule.next_schedule=next_time.strftime("%Y-%m-%d %H:%M:00")
			# print(next_time)
			print(schedule.next_schedule)
			schedule.finish_date=finish_time.strftime("%Y-%m-%d %H:%M:00")
			print(schedule.finish_date)
			schedule.gpio_pin = form.cleaned_data['gpio_pin']
			print(schedule.gpio_pin)
			schedule.save()
			latest = Schedule.objects.all().order_by('-id')
			context = {
				'form': form,
				'waters': latest
			}
			return redirect('/', context)
	# If this is a GET (or any other method) create the default form.
	else:
		form = ScheduleForm(initial={
			'start_date': datetime.today(),
			'start': datetime.now(),
		})
		wat_form = Schedule.objects.all().order_by('-finish')[:3]
		context = {
			'form': form,
			'waters': wat_form,
		}
	return redirect('/', context)
