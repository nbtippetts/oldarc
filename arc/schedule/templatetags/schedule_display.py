from django import template
register = template.Library()
from ..models import Schedule, ScheduleLog, RelayStatus
from ..forms import ScheduleForm, RelayStatusForm
from datetime import datetime
import RPi.GPIO as GPIO

@register.inclusion_tag('gpio_14_schedule_log.html')
def show_gpio_14_schedule_log():
	latest_schedule = ScheduleLog.objects.filter(gpio_pin=14).order_by('-id')[:10]
	if latest_schedule.exists():
		return {'latest_schedule': latest_schedule}
	else:
		no_data = {
			'start': '00:00:00',
			'deration': '00:00:00',
			'finish_date': '00:00:00'
		}
		return {'latest_schedule': no_data}


@register.inclusion_tag('gpio_15_schedule_log.html')
def show_gpio_15_schedule_log():
	latest_schedule = ScheduleLog.objects.filter(gpio_pin=15).order_by('-id')[:10]
	if latest_schedule.exists():
		return {'latest_schedule': latest_schedule}
	else:
		no_data = {
			'start': '00:00:00',
			'deration': '00:00:00',
			'finish_date': '00:00:00'
		}
		return{'latest_schedule': no_data}

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
def gpio_14_state():
	relay_state = RelayStatus.objects.filter(gpio_pin=14).first()
	if not relay_state:
		form = RelayStatusForm(initial={
			'status': False,
		})
		return {'form': form}
	else:
		form = RelayStatusForm(initial={
			'status': relay_state.status,
		})
		return {'form': form}


# @register.inclusion_tag('relay_15.html')
# def gpio_15_state():
# 	form = RelayStatus()
# 	return {'form': form}

@register.inclusion_tag('gpio_14.html')
def gpio_14_state_function():
	pin_state = b'ON'
	if pin_state == b'ON' or schedule_pin_state == b'ON':
		pin_state = 1
	else:
		pin_state = 0
	return {'gpio_14_state':pin_state}

@register.inclusion_tag('gpio_15.html')
def gpio_15_state_function():
	pin_state = b'ON'
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