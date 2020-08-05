from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from datetime import datetime, timedelta
from .models import Water
from .forms import WaterForm
import time


def water(request):
	wat = Water.objects.all().order_by('-water_finish')[:3]
	context = {
		'waters': wat,
	}
	return render(request, 'water/water.html', context)

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
			return redirect('/')
	# If this is a GET (or any other method) create the default form.
	else:
		proposed_water_time = wat.water_finish + timedelta(hours=48)
		form = WaterForm(initial={'water_start': proposed_water_time})
		print(form.cleaned_data['water_start'])
		wat_form = Water.objects.all().order_by('-water_finish')[:3]
	context = {
		'form': form,
		'waters': wat_form,
	}
	return render(request, 'water/water.html', context)
