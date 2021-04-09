from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from datetime import datetime, timedelta, time, date
from .models import Schedule, ScheduleLog
from .forms import ScheduleForm
import time
import json
from django.utils import timezone
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


jobstores = {
  'default': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@db:5432/arc_db')
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
scheduler.start()

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
			print(form.cleaned_data['start'])
			if datetime.now().time() > form.cleaned_data['start']:
				print(form.cleaned_data['how_often'])
				# scheduler.add_job(schedule_relay,'interval', hours=0, minutes=0, seconds=10, id='update_schedule_job_id', replace_existing=True)
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

def schedule_relay():
	return