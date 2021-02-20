from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import HumidityTemp, HumidityTempValues
from .forms import HumidityTempForm
from .hum_temp import get_humidity_temperature
import datetime


def humidity(request):
	return render(request, 'humidity.html')

def set_humidity_temp(request):
	if request.method == 'POST':
		form = HumidityTempForm(request.POST)
		if form.is_valid():
			data = HumidityTempValues.objects.get(pk=1)
			data.humidity_value = form.cleaned_data['humidity_value']
			data.buffer_value = form.cleaned_data['buffer_value']
			data.temp_value = form.cleaned_data['temp_value']
			data.save()
			print('Humidity and Tempature values saved successfully.')
			ht_obj = HumidityTemp.objects.all().order_by('-created_at')[:10]
			context = {'data': ht_obj,'form':form}
			return render(request, 'humidity.html',context)

		ht_obj = HumidityTemp.objects.all().order_by('-created_at')[:10]
		context = {'data': ht_obj,'form':form}
		return render(request, 'humidity.html',context)

def ajax_humidity(request):
	current_humidity, current_temp = get_humidity_temperature()
	return JsonResponse({'current_humidity':current_humidity, 'current_temp':current_temp})