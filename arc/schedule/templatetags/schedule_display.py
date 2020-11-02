from django import template
register = template.Library()
from ..models import Schedule
from humidity.hum_temp import get_humidity_temperature
import RPi.GPIO as GPIO

@register.inclusion_tag('latest_schedule.html')
def show_latest_schedule():
	current_humidity, current_temp = get_humidity_temperature()
	return {'humidity': current_humidity,
		'temp': current_temp,
		'gpio_14_state': gpio_14_state_function(),
		'gpio_15_state': gpio_15_state_function(),
		'gpio_18_state': gpio_18_state_function(),}

def gpio_14_state_function():
	gpio_14 = 14
	GPIO.setmode(GPIO.BCM)  
	# Setup your channel
	GPIO.setup(gpio_14, GPIO.OUT)
	GPIO.output(gpio_14, GPIO.LOW)
	gpio_14_state = GPIO.input(gpio_14)
	return gpio_14_state

def gpio_15_state_function():
	gpio_15 = 15
	GPIO.setmode(GPIO.BCM)  
	# Setup your channel
	GPIO.setup(gpio_15, GPIO.OUT)
	GPIO.output(gpio_15, GPIO.LOW)
	gpio_15_state = GPIO.input(gpio_15)
	return gpio_15_state

def gpio_18_state_function():
	gpio_18 = 18
	GPIO.setmode(GPIO.BCM)  
	# Setup your channel
	GPIO.setup(gpio_18, GPIO.OUT)
	GPIO.output(gpio_18, GPIO.LOW)
	gpio_18_state = GPIO.input(gpio_18)
	return gpio_18_state