from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from datetime import datetime, timedelta
from .models import Water, WaterPump
from .forms import WaterForm, WaterPumpForm
import time
import gpiozero
from gpiozero import LED, Button, Servo
import schedule

def water(request):

	wat = Water.objects.all().order_by('-water_finish')[:3]
	context = {
		'waters': wat,
	}
	return render(request, 'water/water.html', context)

def start_pump(request):
	wat = Water.objects.all().order_by('-water_finish')[:3]
	pump = WaterPump.objects.get(pk=1)
	if request.method == 'POST':
		pump_form = WaterPumpForm(request.POST)
		if pump_form.is_valid():
			pump.pump_status = pump_form.cleaned_data['pump_status']
			pump.save()
			stat = False
			if pump.pump_status == 'start':
				servo = Servo(26)
				servo.max()
			if pump.pump_status == 'stop':
				servo = Servo(26)
				servo.detach()

			context = {
				'waters': wat,
				'form': pump_form
			}
			return render(request, 'water/water_pump.html', context)
	context = {
		'waters': wat,
		'form': pump
	}
	return render(request, 'water/water_pump.html', context)

def check_water(request):
	wat = Water.objects.last()
	# If this is a POST request then process the Form data
	if request.method == 'POST':
		# Create a form instance and populate it with data from the request (binding):
		form = WaterForm(request.POST)
		# Check if the form is valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required (here we just write it to the model due_back field)
			wat.water_start = form.cleaned_data['water_start']
			wat.water_deration = form.cleaned_data['water_deration']
			wat.how_often = form.cleaned_data['how_often']
			wat.save()
			
			# redirect to a new URL:
			return redirect('check-water/')
	# If this is a GET (or any other method) create the default form.
	else:
		proposed_water_time = wat.water_finish + timedelta(hours=48)
		form = WaterForm(initial={'water_start': proposed_water_time})
		print(form['water_start'])
		wat_form = Water.objects.all().order_by('-water_finish')[:3]
	context = {
		'form': form,
		'waters': wat_form,
	}
	return render(request, 'water/water.html', context)
