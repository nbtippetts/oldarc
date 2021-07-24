from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from datetime import datetime, timedelta, time, date
from .models import Schedule, ScheduleLog, RelayStatus
from .forms import ScheduleForm, RelayStatusForm
import time
import gpiozero
import json
from django.utils import timezone
from pytz import utc
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


jobstores = {
  'default': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@db:5432/arc_db')
# 'default': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@localhost:5432/arc_db')
}
executors = {
  'default': ThreadPoolExecutor(10),
  'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
  'coalesce': False,
  'max_instances': 25
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)


def schedule(request):
	schedule_obj = Schedule.objects.all().order_by('-finish')[:3]
	context = {
		'waters': schedule_obj,
	}
	# return redirect('/', context)
	return render(request, 'schedule.html',context)


def update_schedule(request):
	latest = ScheduleLog.objects.all()
	# If this is a POST request then process the Form data
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request (binding):
		form = ScheduleForm(request.POST)
		# Check if the form is valid:
		if form.is_valid():
			start_dt = datetime.combine(date.today(),form.cleaned_data['start'])
			schedule_duration = form.cleaned_data['deration'].split(':')
			print(start_dt)
			if schedule_duration[1][0] == '0':
				time_change = timedelta(hours=int(schedule_duration[0]),minutes=int(schedule_duration[1][1]),seconds=int(schedule_duration[2]))
			else:
				time_change = timedelta(hours=int(schedule_duration[0]),minutes=int(schedule_duration[1]),seconds=int(schedule_duration[2]))
			end_dt = start_dt + time_change
			print(end_dt)
			# if datetime.now().time() > form.cleaned_data['start']:
			print(form.cleaned_data['how_often'])
			schedule_interval = form.cleaned_data['how_often'].split(':')
			print(schedule_interval)
			gpio_num=form.cleaned_data['gpio_pin']
			if schedule_interval[1][0] == '0':
				if gpio_num == '14':
					scheduler.add_job(schedule_relay_14, 'interval', hours=int(schedule_interval[0]), minutes=int(schedule_interval[1][1]), seconds=int(schedule_interval[2]),args=[time_change,gpio_num], id='update_schedule_job_id_14', max_instances=1, replace_existing=True)
				elif gpio_num == '15':
					scheduler.add_job(schedule_relay_15, 'interval', hours=int(schedule_interval[0]), minutes=int(schedule_interval[1][1]), seconds=int(schedule_interval[2]),args=[time_change,gpio_num], id='update_schedule_job_id_15', max_instances=1, replace_existing=True)
				else:
					print('unable to add schedule_relay JOB')
				scheduler.print_jobs()
			else:
				if gpio_num == '14':
					scheduler.add_job(schedule_relay_14,'interval', hours=int(schedule_interval[0]), minutes=int(schedule_interval[1]), seconds=int(schedule_interval[2]),args=[time_change,gpio_num], id='update_schedule_job_id_14', max_instances=1, replace_existing=True)
				elif gpio_num == '15':
					scheduler.add_job(schedule_relay_15,'interval', hours=int(schedule_interval[0]), minutes=int(schedule_interval[1]), seconds=int(schedule_interval[2]),args=[time_change,gpio_num], id='update_schedule_job_id_15', max_instances=1, replace_existing=True)
				else:
					print('unable to add schedule_relay JOB')

				scheduler.print_jobs()
			context = {
				'form': form,
				'waters': latest
			}
			return redirect('/schedule', context)
			# return render(request, 'schedule.html',context)
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
	# return redirect('/', context)
	return render(request, 'schedule.html',context)

def schedule_relay_14(*args):
	print(args)
	print('schedule_relay_job_14 1')
	gpio_num = args[1]
	dt = datetime.now()
	end_dt = dt + args[0]
	print(end_dt)
	schedule_log = ScheduleLog()
	schedule_log.start = datetime.now()
	schedule_log.gpio_pin = gpio_num
	schedule_log.save()
	break_loop = False
	while not break_loop:
		try:
			relay = gpiozero.OutputDevice(int(gpio_num), active_high=False, initial_value=False)
			print('schedule_relay_job_14 relay on')
			relay.on()
		except Exception as e:
			pass
		if end_dt < datetime.now():
			break_loop = True
			schedule_log = ScheduleLog.objects.filter(gpio_pin=14).order_by('-start').first()
			convert_to_time=(datetime.min + args[0]).time()
			schedule_log.deration = convert_to_time
			schedule_log.save()
		time.sleep(1)

def schedule_relay_15(*args):
	print(args)
	print('schedule_relay_job_15 1')
	gpio_num = args[1]
	dt = datetime.now()
	end_dt = dt + args[0]
	print(end_dt)
	schedule_log = ScheduleLog()
	schedule_log.start = datetime.now()
	schedule_log.gpio_pin = gpio_num
	schedule_log.save()
	break_loop = False
	while not break_loop:
		try:
			relay = gpiozero.OutputDevice(int(gpio_num), active_high=False, initial_value=False)
			print('schedule_relay_job_15 relay on')
			relay.on()
		except Exception as e:
			pass
		if end_dt < datetime.now():
			break_loop = True
			schedule_log = ScheduleLog.objects.filter(gpio_pin=15).order_by('-start').first()
			convert_to_time=(datetime.min + args[0]).time()
			schedule_log.deration = convert_to_time
			schedule_log.save()
		time.sleep(1)

def relay_on_off_14(request):
	if request.method == 'POST':
		form = RelayStatusForm(request.POST)
		if form.is_valid():
			status=form.cleaned_data['status']
			gpio_pin=14
			relay = RelayStatus()
			relay.status=status
			relay.gpio_pin=gpio_pin
			relay.save()
			form = RelayStatusForm(initial={
				'status': status,
			})
			return render(request, 'schedule.html',form)
	else:
		relay_state = RelayStatus.objects.filter(gpio_pin=14).first()
		if not relay_state:
			form = RelayStatusForm(initial={
				'status': False,
			})
		else:
			form = RelayStatusForm(initial={
				'status': relay_state.status,
			})
		return render(request, 'schedule.html',form)

# def relay_on_off_15(request):
# 	if request.method == 'POST':
# 		form = RelayStatus(request.POST)
# 		if form.is_valid():
# 			status=form.cleaned_data['status']

# 	return
scheduler.start()