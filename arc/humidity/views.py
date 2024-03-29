from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import HumidityTemp, HumidityTempValues, Exhaust
from .forms import HumidityTempForm, ExhaustForm
from .hum_temp import get_humidity_temperature,stop_relay_18,start_relay_18, stop_auto_relay_18, start_auto_relay_18
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
			print('Humidity and temperature values saved successfully.')
			ht_obj = HumidityTemp.objects.all().order_by('-created_at')[:10]
			context = {'data': ht_obj,'form':form}
			return render(request, 'humidity.html',context)

		ht_obj = HumidityTemp.objects.all().order_by('-created_at')[:10]
		context = {'data': ht_obj,'form':form}
		return render(request, 'humidity.html',context)

def relay_on_off_17_18(request):
	url_path = request.path
	print(url_path)
	url_path = url_path.split('/')
	if request.method == 'POST':
		form = ExhaustForm(request.POST)
		if form.is_valid():
			status=request.POST.get('status')
			auto_status=request.POST.get('auto_status')
			gpio_pin=0
			if request.POST.get('17'):
				pk=1
				gpio_pin=17
			elif request.POST.get('18'):
				pk=2
				gpio_pin=18
				if status == 'False':
					stop_relay_18(gpio_pin)
				elif status == 'True':
					start_relay_18(gpio_pin)
				if auto_status == 'False':
					stop_auto_relay_18(gpio_pin)
				elif auto_status == 'True':
					start_auto_relay_18(gpio_pin)
			else:
				print('No GPIO Pin in args')

			if status is None:
				relay_status = Exhaust.objects.get(pk=pk)
				relay_status.gpio_pin=gpio_pin
				relay_status.automation_status=auto_status
				relay_status.save()
			else:
				relay_status = Exhaust.objects.get(pk=pk)
				relay_status.gpio_pin=gpio_pin
				relay_status.status=status
				relay_status.save()

			form = Exhaust()
			context = {
				'form': form
			}
			return render(request, f'{url_path[1]}.html',context)
		else:
			form = Exhaust()
			context = {
				'form': form
			}
			return render(request, f'{url_path[1]}.html', context)

def ajax_humidity(request):
	current_humidity, current_temp = get_humidity_temperature()
	return JsonResponse({'current_humidity':current_humidity, 'current_temp':current_temp})