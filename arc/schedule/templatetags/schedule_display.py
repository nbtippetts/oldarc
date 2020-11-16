from django import template
register = template.Library()
from ..models import Schedule, ScheduleLog
from ..forms import RelayForm, ScheduleForm
from datetime import datetime
import RPi.GPIO as GPIO
import redis
rdb = redis.Redis(host='redis',port=6379,db=0)
# rdb = redis.Redis(host='redis',port=6379,db=0)
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

@register.inclusion_tag('relay_14.html')
def relay_14():
	stat = rdb.get('gpio_14')
	if stat == b'ON':
		relay_status = False
	else:
		relay_status = True
	form = RelayForm(initial={
		'relay_status': relay_status,
	})
	return {'form': form}

@register.inclusion_tag('relay_15.html')
def relay_15():
	stat = rdb.get('gpio_15')
	if stat == b'ON':
		relay_status = False
	else:
		relay_status = True
	form = RelayForm(initial={
		'relay_status': relay_status,
	})
	return {'form': form}

@register.inclusion_tag('gpio_14.html')
def gpio_14_state_function():
	pin_state = rdb.get('gpio_14')
	schedule_pin_state = rdb.get('schedule_gpio_14')
	if pin_state == b'ON' or schedule_pin_state == b'ON':
		pin_state = 1
	else:
		pin_state = 0
	return {'gpio_14_state':pin_state}

@register.inclusion_tag('gpio_15.html')
def gpio_15_state_function():
	pin_state = rdb.get('gpio_15')
	schedule_pin_state = rdb.get('schedule_gpio_15')
	if pin_state == b'ON' or schedule_pin_state == b'ON':
		pin_state = 1
	else:
		pin_state = 0
	return {'gpio_15_state':pin_state}

@register.inclusion_tag('gpio_18.html')
def gpio_18_state_function():
	if not rdb.exists('gpio_18'):
		rdb.set("gpio_18","OFF")
	pin_state = rdb.get('gpio_18')
	if pin_state == b'ON':
		pin_state = 1
	else:
		pin_state = 0
	return {'gpio_18_state':pin_state}