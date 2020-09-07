from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render
from .models import HumidityTemp

def humidity(request):
	data = HumidityTemp.objects.all().order_by('-created_at')[:10]
	return render(request, 'humidity/line_chart.html', {'data': data})

