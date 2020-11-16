from django import template
register = template.Library()
from ..models import HumidityTemp, HumidityTempValues
from ..forms import HumidityTempForm
from ..hum_temp import get_humidity_temperature
from datetime import datetime

@register.inclusion_tag('humidity.html')
def show_temp_humidity():
	current_humidity, current_temp = get_humidity_temperature()
	return {'humidity': current_humidity,'temp': current_temp}

@register.inclusion_tag('line_chart.html')
def humidity():
	current_humidity, current_temp = get_humidity_temperature()
	form = HumidityTempForm()
	data = HumidityTemp.objects.all().order_by('-created_at')[:6]
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
	# charts_list = []
	# for d in data:
	# 	charts_list.append(d.created_at.strftime("%Y-%m-%d %H:%M:%S"))
	return {'data': data,
	'form':form,
	'current_humidity':current_humidity,
	'current_temp':current_temp,
	'humidity_value':current_values.humidity_value,
	'temp_value':current_values.temp_value,}

@register.inclusion_tag('set_humidity_temp.html')
def humidity_temp_form():
	return humidity()
