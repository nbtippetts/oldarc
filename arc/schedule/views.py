from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from datetime import datetime, timedelta, time, date
from .models import Schedule
from .forms import ScheduleForm
import time
import json
from django.utils import timezone
from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


jobstores = {
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

def relay_on_off_14(request):
	if request.method == 'POST':
		relay_form = RelayForm(request.POST)
		if relay_form.is_valid():
		
			context = {
				'waters': wat,
				'form': relay_form
			}
			# return redirect('/', context)
			return render(request, 'schedule.html',context)
	else:
		form = RelayForm()
		context = {
			'waters': wat,
			'form': form
		}
		# return redirect('/', context)
		return render(request, 'schedule.html',context)

def relay_on_off_15(request):
	if request.method == 'POST':
			context = {
				'waters': wat,
				'form': relay_form
			}
			# return redirect('/', context)
			return render(request, 'schedule.html',context)
	else:
		form = RelayForm()
		context = {
			'waters': wat,
			'form': form
		}
		# return redirect('/', context)
		return render(request, 'schedule.html',context)


def update_schedule(request):
	# If this is a POST request then process the Form data
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request (binding):
		form = ScheduleForm(request.POST)
		# Check if the form is valid:
		if form.is_valid():
			print(form)
			scheduler.add_job('cron', seconds=10, id='update_schedule_job_id', replace_existing=True)
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
