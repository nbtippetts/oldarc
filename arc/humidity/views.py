from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import HumidityTemp, HumidityTempValues
from .forms import HumidityTempForm
from .hum_temp import get_humidity_temperature
import datetime

def humidity(request):
	# current_humidity, current_temp = get_humidity_temperature()
	current_humidity, current_temp = 0.0, 0.0
	form = HumidityTempForm()
	data = HumidityTemp.objects.all().order_by('-created_at')[:10]
	try:
		current_values = HumidityTempValues.objects.get(pk=1)
	except Exception as e:
		h = HumidityTempValues(
			humidity_value=0.0,
			temp_value=0.0
		)
		h.save()
		current_values = HumidityTempValues.objects.get(pk=1)
		pass
	context = {'data': data,
	'form':form,
	'current_humidity':current_humidity,
	'current_temp':current_temp,
	'humidity_value':current_values.humidity_value,
	'temp_value':current_values.temp_value,}
	return render(request, 'line_chart.html', context)

def set_humidity_temp(request):
	if request.method == 'POST':
		form = HumidityTempForm(request.POST)
		if form.is_valid():
			data = HumidityTempValues.objects.get(pk=1)
			data.humidity_value = form.cleaned_data['humidity_value']
			data.temp_value = form.cleaned_data['temp_value']
			data.save()
			print('Humidity and Tempature values saved successfully.')
			form = HumidityTempForm()
			ht_obj = HumidityTemp.objects.all().order_by('-created_at')[:10]
			context = {'data': ht_obj,'form':form}
			return redirect('humidity_view')

		ht_obj = HumidityTemp.objects.all().order_by('-created_at')[:10]
		context = {'data': ht_obj,'form':form}
		return redirect('humidity_view')
