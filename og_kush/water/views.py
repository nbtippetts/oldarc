from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from datetime import datetime, timedelta, time, date
from django_celery_beat.models import PeriodicTasks, PeriodicTask, IntervalSchedule
from .models import Water, WaterPump
from .forms import WaterForm, WaterPumpForm
import time
import json
import gpiozero
from gpiozero import LED, Button, Servo
from .tasks import relay_task, start_water_pump_task

def water(request):
	wat = Water.objects.all().order_by('-water_finish')[:3]
	context = {
		'waters': wat,
	}
	return render(request, 'water/water.html', context)

def start_pump(request):
	wat = Water.objects.all().order_by('-water_finish')[:3]
	if request.method == 'POST':
		pump_form = WaterPumpForm(request.POST)
		if pump_form.is_valid():
			stat = False
			if pump_form.cleaned_data['pump_status'] == 'start':
				water_pump = WaterPump(
					pump_status=pump_form.cleaned_data['pump_status'],
					pump_start = datetime.now(),
					pump_finish=datetime.now(),
					gpio_pin=pump_form.cleaned_data['gpio_pin']
				)
				water_pump.save()
				relay_task.delay(True, pump_form.cleaned_data['gpio_pin'])
				servo = Servo(26)
				servo.max()
			if pump_form.cleaned_data['pump_status'] == 'stop':
				water_pump = WaterPump.objects.filter(
					gpio_pin=pump_form.cleaned_data['gpio_pin']).latest('pump_start')
				water_pump.pump_status = pump_form.cleaned_data['pump_status']
				water_pump.pump_finish = datetime.now()
				water_pump.save()
				relay_task.delay(False, pump_form.cleaned_data['gpio_pin'])
				servo = Servo(26)
				servo.detach()

			context = {
				'waters': wat,
				'form': pump_form
			}
			return render(request, 'water/water_pump.html', context)
	form = WaterPumpForm(initial={
		'pump_status': 'stop',
	})
	context = {
		'waters': wat,
		'form': form
	}
	return render(request, 'water/water_pump.html', context)

def check_water(request):
	# If this is a POST request then process the Form data
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request (binding):
		form = WaterForm(request.POST)
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
					task=form.cleaned_data['task_name'],
					kwargs=json.dumps({
						'pin': form.cleaned_data['gpio_pin'],
						'deration': form.cleaned_data['water_deration']
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
				date.min, form.cleaned_data['water_start']) - datetime.min
			t = datetime.today()
			format_water_duration = t.strftime(
				'%Y-%m-%d')+' '+form.cleaned_data['water_deration']
			wd = datetime.strptime(
				format_water_duration, '%Y-%m-%d %H:%M:%S')
			finish_time = ws + wd
			print(finish_time)
			often = datetime.strptime(
				form.cleaned_data['how_often'], '%H:%M:%S')
			nw = datetime.combine(
				date.min, often.time()) - datetime.min
			next_water_time = finish_time + nw
			print(next_water_time)
			water = Water(
				water_start_date=form.cleaned_data['water_start_date'],
				water_start = form.cleaned_data['water_start'],
				how_often = form.cleaned_data['how_often'],
				water_deration = form.cleaned_data['water_deration'],
				water_finish = finish_time,
				next_water=next_water_time,
				gpio_pin = form.cleaned_data['gpio_pin']
			)
			water.save()
			time.sleep(2)
			start_water_pump_task.delay()
			water_latest = Water.objects.all().order_by('-id')
			context = {
				'form': form,
				'waters': water_latest
			}
			return render(request, 'water/check_water.html', context)
	# If this is a GET (or any other method) create the default form.
	else:
		wat = Water.objects.last()
		wat.water_start_date = datetime.today()
		wat.water_start = datetime.now()
		form = WaterForm(initial={
			'water_start_date': wat.water_start_date,
			'water_start': wat.water_start,
		})
		print(form['water_start'])
		wat_form = Water.objects.all().order_by('-water_finish')[:3]
		context = {
			'form': form,
			'waters': wat_form,
		}
	return render(request, 'water/check_water.html', context)
