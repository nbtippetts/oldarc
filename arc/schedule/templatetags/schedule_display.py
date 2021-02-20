from django import template
register = template.Library()
from ..models import Schedule, ScheduleLog
from ..forms import ScheduleForm
from datetime import datetime
import RPi.GPIO as GPIO

@register.inclusion_tag('gpio_14_schedule_log.html')
def show_gpio_14_schedule_log():
	latest_schedule = ScheduleLog.objects.filter(gpio_pin=14).order_by('-id')[:10]
	return {'latest_schedule': latest_schedule}

@register.inclusion_tag('gpio_15_schedule_log.html')
def show_gpio_15_schedule_log():
	latest_schedule = ScheduleLog.objects.filter(gpio_pin=15).order_by('-id')[:10]
	return {'latest_schedule': latest_schedule}

@register.inclusion_tag('gpio_14_schedule.html')
def show_gpio_14_schedule():
	latest_schedule = Schedule.objects.filter(gpio_pin=14)
	return {'latest_schedule': latest_schedule}

@register.inclusion_tag('gpio_15_schedule.html')
def show_gpio_15_schedule():
	latest_schedule = Schedule.objects.filter(gpio_pin=15)
	return {'latest_schedule': latest_schedule}

@register.inclusion_tag('update_schedule.html')
def schedule_form():
	form = ScheduleForm(initial={
		'start_date': datetime.today(),
		'start': datetime.now(),
	})
	return {'form': form}

@register.inclusion_tag('gpio_14.html')
def gpio_14_state_function():
	if pin_state == b'ON' or schedule_pin_state == b'ON':
		pin_state = 1
	else:
		pin_state = 0
	return {'gpio_14_state':pin_state}

@register.inclusion_tag('gpio_15.html')
def gpio_15_state_function():
	if pin_state == b'ON' or schedule_pin_state == b'ON':
		pin_state = 1
	else:
		pin_state = 0
	return {'gpio_15_state':pin_state}

@register.inclusion_tag('gpio_18.html')
def gpio_18_state_function():
	if pin_state == b'ON':
		pin_state = 1
	else:
		pin_state = 0
	return {'gpio_18_state':pin_state}