from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from datetime import datetime, timedelta, time, date
from django_celery_beat.models import PeriodicTasks, PeriodicTask, IntervalSchedule
from .models import Schedule, Relay, Relay14, Relay15
from .forms import ScheduleForm, RelayForm, RelayForm14, RelayForm15
import time
import json
from .tasks import relay_task_14, relay_task_15
import redis

# rdb = redis.Redis(host='redis',port=6379,db=0)
rdb = redis.Redis(host='localhost',port=6379,db=0)


def schedule(request):
	schedule_obj = Schedule.objects.all().order_by('-finish')[:3]
	context = {
		'waters': schedule_obj,
	}
	return render(request, 'base.html', context)

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
					relay_task_14.delay(False, 14)
				except Exception as e:
					pass

			context = {
				'waters': wat,
				'form': relay_form
			}
			return render(request, 'base.html', context)
	else:
		form = RelayForm()
		context = {
			'waters': wat,
			'form': form
		}
		return render(request, 'base.html', context)

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
					relay_task_15.delay(False, 15)
				except Exception as e:
					pass

			context = {
				'waters': wat,
				'form': relay_form
			}
			return render(request, 'base.html', context)
	else:
		form = RelayForm()
		context = {
			'waters': wat,
			'form': form
		}
		return render(request, 'base.html', context)


def check_schedule(request):
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
				format_duration, '%Y-%m-%d %H:%M:%S')
			finish_time = ws + wd
			print(finish_time)
			often = datetime.strptime(
				form.cleaned_data['how_often'], '%H:%M:%S')
			nw = datetime.combine(
				date.min, often.time()) - datetime.min
			next_time = finish_time + nw
			print(next_time)
			schedule = Schedule.objects.get(gpio_pin=form.cleaned_data['gpio_pin'])
			schedule.start_date=form.cleaned_data['start_date'],
			schedule.start = form.cleaned_data['start'],
			schedule.how_often = form.cleaned_data['how_often'],
			schedule.deration = form.cleaned_data['deration'],
			schedule.finish = finish_time,
			schedule.next_schedule=next_time,
			schedule.gpio_pin = form.cleaned_data['gpio_pin']
			
			schedule.save()
			latest = Schedule.objects.all().order_by('-id')
			context = {
				'form': form,
				'waters': latest
			}
			return render(request, 'base.html', context)
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
	return render(request, 'base.html', context)
