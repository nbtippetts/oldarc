import Adafruit_DHT
import gpiozero
import time
from datetime import datetime, timedelta
from .models import HumidityTemp, HumidityTempValues, Exhaust
from pytz import utc
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


jobstores = {
  'default': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@db:5432/arc_db')
#   'default': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@localhost:5432/arc_db')
}
executors = {
  'default': ThreadPoolExecutor(10),
  'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
  'coalesce': True,
  'max_instances': 25
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

def stop_auto_relay_18(gpio_pin):
	scheduler.pause_job('humidity_temp_job_id')
	scheduler.print_jobs()
	return
def start_auto_relay_18(gpio_pin):
	scheduler.resume_job('humidity_temp_job_id')
	scheduler.print_jobs()
	return
def stop_relay_18(gpio_pin):
	scheduler.pause_job('exhaust_job_id')
	scheduler.print_jobs()
	return
def start_relay_18(gpio_pin):
	scheduler.resume_job('exhaust_job_id')
	scheduler.print_jobs()
	return
def get_humidity_temperature():
	sensor = Adafruit_DHT.DHT22
	pin =4
	new_humidity = 0.0
	new_temperature = 0.0
	for i in range(2):
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		if humidity is not None and temperature is not None:
			new_humidity = "{0:0.1f}%".format(humidity)
			fahrenheit = (temperature * 9/5) + 32
			fahrenheit=str(fahrenheit).split('.')
			new_temperature = fahrenheit[0]+'*F'
			break
		else:
			print('Failed to retrieve data from humidity sensor.')
			continue
	print(new_humidity,new_temperature)
	return new_humidity, new_temperature

def humidity_temperature_logs():
	sensor = Adafruit_DHT.DHT22
	pin =4
	while True:
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		if humidity is not None and temperature is not None:
			fahrenheit = (temperature * 9/5) + 32
			fahrenheit=str(fahrenheit).split('.')
			new_temperature = fahrenheit[0]
			ht_log = HumidityTemp()
			ht_log.humidity = humidity
			ht_log.temp = new_temperature
			ht_log.save()
			break
		else:
			print('Failed to retrieve data from humidity sensor.')
			continue

def exhaust_relay_job():
	try:
		while True:
			try:
				try:
					e = Exhaust.objects.get(pk=2)
				except Exception as ex:
					e = Exhaust()
					e.pk=2
					e.job_id='exhaust_job_id'
					e.gpio_pin=18
					e.status=False
					e.save()
				e = Exhaust.objects.get(pk=2)
				if e.status == 'True':
					try:
						relay = gpiozero.OutputDevice(18, active_high=False, initial_value=False)
						print('exhaust_job_id relay on')
						relay.on()
					except Exception as e:
						pass
				else:
					break
				time.sleep(5)
			except Exception as e:
				e = Exhaust(pk=2, job_id='exhaust_job_id', status=False)
				e.save()
	except Exception as e:
		print(e)
		print('exhaust_relay_job 3')
		e = Exhaust(pk=2, job_id='exhaust_job_id', status=False)
		e.save()

def humidifer_relay_job():
	try:
		while True:
			try:
				try:
					e = Exhaust.objects.get(pk=1)
				except Exception as ex:
					e = Exhaust()
					e.pk=1
					e.job_id='exhaust_job_id'
					e.gpio_pin=17
					e.status=False
					e.save()
				e = Exhaust.objects.get(pk=1)
				if e.status == 'True':
					try:
						relay = gpiozero.OutputDevice(17, active_high=False, initial_value=False)
						print(' humidifer_relay_job relay on')
						relay.on()
					except Exception as e:
						pass
				else:
					break
				time.sleep(5)
			except Exception as e:
				e = Exhaust(pk=1, job_id='humidifer_job_id', status=False)
				e.save()
	except Exception as e:
		print(e)
		print('humidifer_relay_job 3')
		e = Exhaust(pk=1, job_id='humidifer_job_id', status=False)
		e.save()


def check_hum_temp():
	sensor = Adafruit_DHT.DHT22
	pin =4
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
		new_humidity = "{0:0.1f}%".format(humidity)
		fahrenheit = (temperature * 9/5) + 32
		new_temperature = "{0:0.1f}*F".format(fahrenheit)
		print(new_humidity, new_temperature)
		try:
			ht_params = HumidityTempValues.objects.get(pk=1)
		except Exception as e:
			ht_params = HumidityTempValues()
			ht_params.pk=1
			ht_params.humidity_value=0.00
			ht_params.buffer_value=0.00
			ht_params.temp_value=0.00
			ht_params.save()
		ht_params = HumidityTempValues.objects.get(pk=1)
		print(ht_params.humidity_value,ht_params.buffer_value, ht_params.temp_value)
		humidity_positive = ht_params.humidity_value+ht_params.buffer_value
		humidity_nagitive = ht_params.humidity_value-ht_params.buffer_value
		temp_params = ht_params.temp_value+ht_params.buffer_value
		print(humidity_positive, humidity_nagitive, temp_params)
		if humidity >= float(humidity_positive):
			try:
				e = Exhaust.objects.get(pk=2)
				if e.auto_status == 'True':
					e.job_id='exhaust_job_id'
					e.status=True
					e.save()
					scheduler.resume_job('exhaust_job_id')
					return
				else:
					e.job_id='exhaust_job_id'
					e.status=False
					e.save()
					scheduler.pause_job('exhaust_job_id')
					return
			except Exception as e:
				e = Exhaust(pk=2, job_id='exhaust_job_id', status=True)
				e.save()

		elif fahrenheit >= float(temp_params):
			try:
				e = Exhaust.objects.get(pk=2)
				e.job_id='exhaust_job_id'
				e.status=True
				e.save()
				print(scheduler.get_job('exhaust_job_id'))
				scheduler.resume_job('exhaust_job_id')
			except Exception as e:
				e = Exhaust(pk=2, job_id='exhaust_job_id', status=True)
				e.save()
		else:
			try:
				e = Exhaust.objects.get(pk=2)
				e.job_id='exhaust_job_id'
				e.status=False
				e.save()
				scheduler.pause_job('exhaust_job_id')
			except Exception as e:
				e = Exhaust(pk=2, job_id='exhaust_job_id', status=False)
				e.save()

	else:
		print('Failed to retrieve data from humidity sensor.')

def check_hum():
	sensor = Adafruit_DHT.DHT22
	pin =4
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
		new_humidity = "{0:0.1f}%".format(humidity)
		fahrenheit = (temperature * 9/5) + 32
		new_temperature = "{0:0.1f}*F".format(fahrenheit)
		print(new_humidity, new_temperature)
		try:
			ht_params = HumidityTempValues.objects.get(pk=1)
		except Exception as e:
			ht_params = HumidityTempValues()
			ht_params.pk=1
			ht_params.humidity_value=0.00
			ht_params.buffer_value=0.00
			ht_params.temp_value=0.00
			ht_params.save()
		ht_params = HumidityTempValues.objects.get(pk=1)
		print(ht_params.humidity_value,ht_params.buffer_value, ht_params.temp_value)
		humidity_positive = ht_params.humidity_value+ht_params.buffer_value
		humidity_nagitive = ht_params.humidity_value-ht_params.buffer_value
		temp_params = ht_params.temp_value+ht_params.buffer_value
		print(humidity_positive, humidity_nagitive, temp_params)
		if humidity <= humidity_nagitive:
			try:
				e = Exhaust.objects.get(pk=1)
				e.job_id='humidifer_job_id'
				e.status=True
				e.save()
				scheduler.resume_job('humidifer_job_id')
			except Exception as e:
				e = Exhaust(pk=1, job_id='humidifer_job_id', status=True)
				e.save()
		else:
			try:
				e = Exhaust.objects.get(pk=1)
				e.job_id='humidifer_job_id'
				e.status=False
				e.save()
			
				scheduler.pause_job('humidifer_job_id')
			except Exception as e:
				e = Exhaust(pk=1, job_id='humidifer_job_id', status=False)
				e.save()

	else:
		print('Failed to retrieve data from humidity sensor.')



scheduler.add_job(check_hum_temp, 'interval', seconds=5, id='humidity_temp_job_id', max_instances=2, replace_existing=True)
scheduler.add_job(check_hum, 'interval', seconds=5, id='check_humidity_job_id', max_instances=2, replace_existing=True)
scheduler.add_job(exhaust_relay_job, 'interval', seconds=9, id='exhaust_job_id', max_instances=1, replace_existing=True)
scheduler.add_job(humidifer_relay_job, 'interval', seconds=9, id='humidifer_job_id', max_instances=1, replace_existing=True)
scheduler.add_job(humidity_temperature_logs, 'interval', seconds=300, id='humidity_temperature_logs_job_id', max_instances=1, replace_existing=True)
scheduler.start()

# @atexit.register
# def goodbye_humidity():
# 	print('shut down scheduler')
# 	scheduler.shutdown()