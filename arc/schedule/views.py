from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from datetime import datetime, timedelta, time, date
from .models import Schedule, ScheduleLog
from .forms import ScheduleForm
import time
import gpiozero
import json
from django.utils import timezone
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


jobstores = {
#   'default': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@db:5432/arc_db')
'default': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@localhost:5432/arc_db')
}
executors = {
  'default': ThreadPoolExecutor(20),
  'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
  'coalesce': False,
  'max_instances': 2
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
				time_change = timedelta(hours=int(schedule_duration[0]),minutes=int(schedule_duration[1][1]),seconds=int(schedule_interval[2]))
			else:
				time_change = timedelta(hours=int(schedule_duration[0]),minutes=int(schedule_duration[1]),seconds=int(schedule_interval[2]))
			end_dt = start_dt + time_change
			print(end_dt)
			# if datetime.now().time() > form.cleaned_data['start']:
			print(form.cleaned_data['how_often'])
			schedule_interval = form.cleaned_data['how_often'].split(':')
			print(schedule_interval)
			if schedule_interval[1][0] == '0':
				scheduler.add_job(schedule_relay(time_change),'interval', hours=int(schedule_interval[0]), minutes=int(schedule_interval[1][1]), seconds=int(schedule_interval[2]), id='update_schedule_job_id', replace_existing=True)
				# scheduler.add_job(schedule_relay,'interval', hours=int(schedule_interval[0]), minutes=int(schedule_interval[1][1]), seconds=int(schedule_interval[2]), id='update_schedule_job_id', replace_existing=True)
				# scheduler.start()
				scheduler.print_jobs()
			else:
				scheduler.add_job(schedule_relay(time_change),'interval', hours=int(schedule_interval[0]), minutes=int(schedule_interval[1]), seconds=int(schedule_interval[2]), id='update_schedule_job_id', replace_existing=True)
				# scheduler.start()
				scheduler.print_jobs()
			context = {
				'form': form,
				'waters': latest
			}
			# return redirect('/', context)
			return render(request, 'schedule.html',context)
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

def schedule_relay(time_change):
	print('schedule_relay_job 1')
	dt = datetime.now()
	end_dt = dt + time_change
	scheduler.add_job(schedule_duration,args=['text'])
	while True:
		try:
			relay = gpiozero.OutputDevice(14, active_high=False, initial_value=False)
			print('schedule_relay_job relay on')
			relay.on()
		except Exception as e:
			pass
		time.sleep(5)

	

# scheduler.start()