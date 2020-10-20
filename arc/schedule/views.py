from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from datetime import datetime, timedelta, time, date
from django_celery_beat.models import PeriodicTasks, PeriodicTask, IntervalSchedule
from .models import Schedule, WaterPump
from .forms import ScheduleForm, WaterPumpForm
import time
import json
from .tasks import relay_task, start_task

def schedule(request):
	schedule_obj = Schedule.objects.all().order_by('-finish')[:3]
	context = {
		'waters': schedule_obj,
	}
	return render(request, 'schedule/schedule.html', context)

def relay_on_off(request):
	wat = Schedule.objects.all().order_by('-finish')[:3]
	if request.method == 'POST':
		pump_form = WaterPumpForm(request.POST)
		if pump_form.is_valid():
			stat = False
			if pump_form.cleaned_data['relay_status'] == 'True':
				water_pump = WaterPump(
					pump_status=pump_form.cleaned_data['relay_status'],
					pump_start = datetime.now(),
					pump_finish=datetime.now(),
					gpio_pin=pump_form.cleaned_data['gpio_pin']
				)
				water_pump.save()
				relay_task.delay(True, pump_form.cleaned_data['gpio_pin'])
			if pump_form.cleaned_data['relay_status'] == 'False':
				try:
					water_pump = WaterPump.objects.filter(
						gpio_pin=pump_form.cleaned_data['gpio_pin']).latest('pump_start')
					water_pump.pump_status = pump_form.cleaned_data['relay_status']
					water_pump.pump_finish = datetime.now()
					water_pump.save()
					relay_task.delay(False, pump_form.cleaned_data['gpio_pin'])
				except Exception as e:
					pass

			context = {
				'waters': wat,
				'form': pump_form
			}
			return render(request, 'schedule/relay.html', context)
	form = WaterPumpForm(initial={
		'relay_status': 'False',
	})
	context = {
		'waters': wat,
		'form': form
	}
	return render(request, 'schedule/relay.html', context)


def check_schedule(request):
	# If this is a POST request then process the Form data
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request (binding):
		form = ScheduleForm(request.POST)
		# Check if the form is valid:
		if form.is_valid():
			get_hour = form.cleaned_data['how_often'].split(':')
			schedule, created = IntervalSchedule.objects.get_or_create(
				every=int(get_hour[0]),
				period=IntervalSchedule.HOURS,
			)
			try:
				p = PeriodicTask.objects.get_or_create(
					interval=schedule,
					name=form.cleaned_data['name'],
					task='schedule.tasks.start_task',
					kwargs=json.dumps({
						'pin': form.cleaned_data['gpio_pin'],
						'deration': form.cleaned_data['deration']
					})
				)
				PeriodicTasks.changed(p)
			except Exception as e:
				p = PeriodicTask.objects.get(name=form.cleaned_data['name'])
				p.interval=schedule
				p.save()
				PeriodicTasks.changed(p)
				pass
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
			schedule = Schedule(
				start_date=form.cleaned_data['start_date'],
				start = form.cleaned_data['start'],
				how_often = form.cleaned_data['how_often'],
				deration = form.cleaned_data['deration'],
				finish = finish_time,
				next_schedule=next_time,
				gpio_pin = form.cleaned_data['gpio_pin']
			)
			schedule.save()
			time.sleep(2)
			start_task.delay()
			latest = Schedule.objects.all().order_by('-id')
			context = {
				'form': form,
				'waters': latest
			}
			return render(request, 'schedule/check_schedule.html', context)
	# If this is a GET (or any other method) create the default form.
	else:
		wat = Schedule.objects.last()
		wat.start_date = datetime.today()
		wat.start = datetime.now()
		form = ScheduleForm(initial={
			'start_date': wat.start_date,
			'start': wat.start,
		})
		print(form['start'])
		wat_form = Schedule.objects.all().order_by('-finish')[:3]
		context = {
			'form': form,
			'waters': wat_form,
		}
	return render(request, 'schedule/check_schedule.html', context)
