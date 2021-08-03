from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from datetime import datetime, timedelta, time, date
from .models import Schedule, ScheduleLog, RelayStatus
from .forms import ScheduleForm, RelayStatusForm
import time
import gpiozero
import json
import threading
from django.utils import timezone
from pytz import utc

def schedule(request):
	start = datetime.now()
	dtwithoutseconds = start.replace(second=0, microsecond=0)
	form = ScheduleForm(initial={
		'start': dtwithoutseconds
	})
	ScheduleLog.objects.filter(duration=None).delete()
	# schedule_obj = Schedule.objects.all().order_by('-finish')[:3]
	context = {
		'form': form
	}
	return render(request, 'schedule.html',context)


def update_schedule(request):
	latest = ScheduleLog.objects.all()
	# If this is a POST request then process the Form data
	if request.method == 'POST':
		form = ScheduleForm(request.POST)
		if form.is_valid():
			schedule_duration = form.cleaned_data['duration']
			start_dt = datetime.combine(date.today(),form.cleaned_data['start'])
			end_dt = start_dt + schedule_duration
			print(end_dt)
			print(form.cleaned_data['how_often'])
			schedule_interval = form.cleaned_data['how_often']
			print(schedule_interval.seconds)
			gpio_pin=form.cleaned_data['gpio_pin']
			pk='0'
			if gpio_pin == '14':
				pk='14'
			else:
				pk='15'
			count = 0

			duration_hours = form.cleaned_data['duration_hours']
			duration_minutes = form.cleaned_data['duration_minutes']
			duration_seconds = form.cleaned_data['duration_seconds']
			if duration_hours == '0':
				duration_display = f'For {duration_minutes} Minutes'
			elif duration_minutes == '0':
				duration_display = f'For {duration_hours} Hours'
			elif duration_hours == '0' and duration_minutes == '0':
				duration_display = f'For {duration_seconds} Seconds'
			else:
				duration_display = f'For {duration_hours} Hours {duration_minutes} Minutes'

			if schedule_interval.days == 1:
				how_often_display = f'Run Every {schedule_interval.days} days'
			else:
				how_often_seconds = schedule_interval.seconds
				how_often_hours = how_often_seconds//3600
				how_often_minutes = (how_often_seconds//60)%60
				if how_often_hours == 0:
					how_often_display = f'Run Every {how_often_minutes} Minutes'
				elif how_often_minutes == 0:
					how_often_display = f'Run Every {how_often_hours} Hours'
				elif how_often_hours == 0 and how_often_minutes == 0:
					how_often_display = f'Run Every {how_often_seconds} Seconds'
				else:
					how_often_display = f'Run Every {how_often_hours} Hours {how_often_minutes} Minutes'

			try:
				set_schedule = Schedule.objects.get(pk=pk)
				set_schedule.duration=duration_display
				set_schedule.schedule_interval=how_often_display
				set_schedule.gpio_pin=gpio_pin
				set_schedule.save()
			except Exception as e:
				set_schedule = Schedule()
				set_schedule.pk=pk
				set_schedule.duration=duration_display
				set_schedule.schedule_interval=how_often_display
				set_schedule.gpio_pin=gpio_pin
				set_schedule.save()
		
			schedule_job_id = f'update_schedule_job_id_{gpio_pin}'
			scheduler.add_job(schedule_relay, 'interval', seconds=schedule_interval.seconds,start_date=start_dt, args=[schedule_duration,gpio_pin,False,schedule_interval.seconds], id=schedule_job_id,max_instances=10, replace_existing=True)
			context = {
				'form': form
			}
			return redirect('/schedule', context)

	else:
		form = ScheduleForm()

	wat_form = Schedule.objects.all().order_by('-finish')[:3]
	context = {
		'form': form
	}
	return render(request, 'schedule.html',context)

def schedule_relay(*args):
	print('schedule_relay_job 1')
	gpio_pin = args[1]
	if gpio_pin == '14':
		pk=1
	elif gpio_pin == '15':
		pk=2
	else:
		print('No GPIO Pin in args')
	
	dt = datetime.now()
	end_dt = dt + args[0]
	relay_status = RelayStatus.objects.get(pk=pk)
	relay_status.schedule_status=True
	relay_status.gpio_pin=gpio_pin
	relay_status.save()
	schedule_log = ScheduleLog()
	schedule_log.start = datetime.now()
	schedule_log.gpio_pin = gpio_pin
	schedule_log.save()
	break_loop = args[2]
	while not break_loop:
		relay_status = RelayStatus.objects.get(pk=pk)
		try:
			relay = gpiozero.OutputDevice(int(gpio_pin), active_high=False, initial_value=False)
			print('schedule_relay_job relay on')
			relay.on()
		except Exception as e:
			pass
		if relay_status.button_status == 'False' and relay_status.schedule_status == 'False':
			break_loop = True
			relay_status = RelayStatus.objects.get(pk=pk)
			relay_status.schedule_status=False
			relay_status.gpio_pin=gpio_pin
			relay_status.save()
			schedule_log = ScheduleLog.objects.filter(gpio_pin=gpio_pin).order_by('-start').first()
			convert_to_time=(datetime.min + args[0]).time()
			schedule_log.duration = str(convert_to_time)
			schedule_log.save()
		if end_dt < datetime.now():
			break_loop = True
			relay_status = RelayStatus.objects.get(pk=pk)
			relay_status.schedule_status=False
			relay_status.gpio_pin=gpio_pin
			relay_status.save()
			schedule_log = ScheduleLog.objects.filter(gpio_pin=gpio_pin).order_by('-start').first()
			convert_to_time=(datetime.min + args[0]).time()
			schedule_log.duration = str(convert_to_time)
			schedule_log.save()
		time.sleep(1)

def relay_on_off(request):
	if request.method == 'POST':
		form = RelayStatusForm(request.POST)
		if form.is_valid():
			status=request.POST.get('status')
			gpio_pin=0
			if request.POST.get('14'):
				pk=1
				gpio_pin=14
			elif request.POST.get('15'):
				pk=2
				gpio_pin=15
			else:
				print('No GPIO Pin in args')
			button_job = scheduler.get_job('button_relay_job_id_14')
			relay_status = RelayStatus.objects.get(pk=pk)
			relay_status.gpio_pin=gpio_pin
			if status == 'False':
				relay_status.schedule_status=status
				relay_status.button_status=status
			else:
				relay_status.button_status=status

			relay_status.save()
			scheduler.print_jobs()
			form = ScheduleForm()
			context = {
				'form': form
			}
			return render(request, 'schedule.html',context)
	else:
		form = ScheduleForm()
	context = {
		'form': form
	}
	return render(request, 'schedule.html',form)

def relay_14():
	try:
		relay = gpiozero.OutputDevice(14, active_high=False, initial_value=False)
		while True:
			try:
				try:
					relay_status = RelayStatus.objects.get(pk=1)
				except Exception as e:
					relay_status = RelayStatus()
					relay_status.pk=1
					relay_status.button_status=False
					relay_status.gpio_pin=14
					relay_status.schedule_status=False
					relay_status.save()
				relay_status = RelayStatus.objects.get(pk=1)
				if relay_status.button_status == 'True' and relay_status.schedule_status == 'False':
					try:
						print(' button_relay_14 relay ON')
						relay.on()
					except Exception as e:
						print(e)
						pass
				elif relay_status.button_status == 'True' and relay_status.schedule_status == 'True':
					break
				else:
					# relay.off()
					break
				time.sleep(1)
			except Exception as e:
				print(e)
				pass
	except Exception as e:
		print(e)
		pass

def relay_15():
	try:
		relay = gpiozero.OutputDevice(15, active_high=False, initial_value=False)
		while True:
			try:
				try:
					relay_status = RelayStatus.objects.get(pk=2)
				except Exception as e:
					relay_status = RelayStatus()
					relay_status.pk=2
					relay_status.button_status=False
					relay_status.gpio_pin=15
					relay_status.schedule_status=False
					relay_status.save()
				relay_status = RelayStatus.objects.get(pk=2)
				if relay_status.button_status == 'True' and relay_status.schedule_status == 'False':
					try:
						print(' button_relay_15 relay ON')
						relay.on()
					except Exception as e:
						print(e)
						pass
				elif relay_status.button_status == 'True' and relay_status.schedule_status == 'True':
					break
				else:
					# relay.off()
					break
				time.sleep(1)
			except Exception as e:
				print(e)
				pass
	except Exception as e:
		print(e)
		pass
