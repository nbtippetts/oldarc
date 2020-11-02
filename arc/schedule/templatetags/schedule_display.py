from django import template
register = template.Library()
from ..models import Schedule
from ..forms import WaterPumpForm
import RPi.GPIO as GPIO

@register.inclusion_tag('gpio_14_schedule.html')
def show_gpio_14_schedule():
	latest_schedule = Schedule.objects.filter(gpio_pin=14)
	return {'latest_schedule': latest_schedule}

@register.inclusion_tag('gpio_15_schedule.html')
def show_gpio_15_schedule():
	latest_schedule = Schedule.objects.filter(gpio_pin=15)
	return {'latest_schedule': latest_schedule}

@register.inclusion_tag('relay.html')
def relay_form():
	form = WaterPumpForm(initial={
		'relay_status': 'False',
	})
	return {'form': form}

@register.inclusion_tag('gpio_14.html')
def gpio_14_state_function():
	gpio_14 = 14
	GPIO.setmode(GPIO.BCM)  
	# Setup your channel
	GPIO.setup(gpio_14, GPIO.OUT)
	GPIO.output(gpio_14, GPIO.LOW)
	gpio_14_state = GPIO.input(gpio_14)
	return {'gpio_14_state':gpio_14_state}

@register.inclusion_tag('gpio_15.html')
def gpio_15_state_function():
	gpio_15 = 15
	GPIO.setmode(GPIO.BCM)  
	# Setup your channel
	GPIO.setup(gpio_15, GPIO.OUT)
	GPIO.output(gpio_15, GPIO.LOW)
	gpio_15_state = GPIO.input(gpio_15)
	return {'gpio_15_state':gpio_15_state}

@register.inclusion_tag('gpio_18.html')
def gpio_18_state_function():
	gpio_18 = 18
	GPIO.setmode(GPIO.BCM)  
	# Setup your channel
	GPIO.setup(gpio_18, GPIO.OUT)
	GPIO.output(gpio_18, GPIO.LOW)
	gpio_18_state = GPIO.input(gpio_18)
	return {'gpio_18_state':gpio_18_state}