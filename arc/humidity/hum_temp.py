import Adafruit_DHT
import gpiozero
import time
from datetime import datetime, timedelta
import gpiozero
from .models import HumidityTemp, HumidityTempValues, Exhust
from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


jobstores = {
  'default': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@db:5432/arc_db')
}
executors = {
  'default': ThreadPoolExecutor(20),
  'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
  'coalesce': False,
  'max_instances': 4
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

def get_humidity_temperature():
	sensor = Adafruit_DHT.DHT22
	pin =4
	new_humidity = 0.0
	new_temperature = 0.0
	for i in range(2):
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		if humidity is not None and temperature is not None:
			new_humidity = "{0:0.1f}%".format(humidity)
			new_temperature = "{0:0.1f}*C".format(temperature)
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
			ht_log = HumidityTemp()
			ht_log.humidity = humidity
			ht_log.temp = temperature
			ht_log.save()
			break
		else:
			print('Failed to retrieve data from humidity sensor.')
			continue

def exhust_relay_job():
	print('exhust_relay_job 1')
	try:
		while True:
			e = Exhust.objects.get(pk=1)
			print('exhust_relay_job 2')
			print(e.status)
			if e.status == 'True':
				try:
					relay = gpiozero.OutputDevice(18, active_high=False, initial_value=False)
					print('exhust_job_id relay on')
					relay.on()
				except Exception as e:
					pass
				# exhust_relay(True)
			else:
				break
			time.sleep(5)
	except Exception as e:
		print(e)
		print('exhust_relay_job 3')
		e = Exhust(pk=1, job_id='exhust_job_id', status=False)
		e.save()

def humidifer_relay_job():
	print('humidifer_relay_job 1')
	try:
		while True:
			e = Exhust.objects.get(pk=2)
			print('humidifer_relay_job 2')
			print(e.status)
			if e.status == 'True':
				try:
					relay = gpiozero.OutputDevice(17, active_high=False, initial_value=False)
					print(' humidifer_relay_job relay on')
					relay.on()
				except Exception as e:
					pass
				# exhust_relay(True)
			else:
				break
			time.sleep(5)
	except Exception as e:
		print(e)
		print('humidifer_relay_job 3')
		e = Exhust(pk=2, job_id='humidifer_job_id', status=False)
		e.save()


def check_hum_temp():
	sensor = Adafruit_DHT.DHT22
	pin =4
	# while True:
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	if humidity is not None and temperature is not None:
		new_humidity = "{0:0.1f}%".format(humidity)
		new_temperature = "{0:0.1f}*C".format(temperature)
		print(new_humidity, new_temperature)
		ht_params = HumidityTempValues.objects.get(pk=1)
		print(ht_params.humidity_value,ht_params.buffer_value, ht_params.temp_value)
		humidity_positive = ht_params.humidity_value+ht_params.buffer_value
		humidity_nagitive = ht_params.humidity_value-ht_params.buffer_value
		temp_params = ht_params.temp_value+ht_params.buffer_value
		print(humidity_positive, humidity_nagitive, temp_params)
		if humidity >= humidity_positive or temperature >= temp_params:
			scheduler.print_jobs()
			try:
				e = Exhust.objects.get(pk=1)
				e.job_id='exhust_job_id'
				e.status=True
				e.save()
				scheduler.resume_job('exhust_job_id')
				# time.sleep(5)
			except Exception as e:
				e = Exhust(pk=1, job_id='exhust_job_id', status=True)
				e.save()
				# time.sleep(5)
		else:
			try:
				e = Exhust.objects.get(pk=1)
				e.job_id='exhust_job_id'
				e.status=False
				e.save()
				scheduler.print_jobs()
				scheduler.pause_job('exhust_job_id')
				# time.sleep(5)
			except Exception as e:
				e = Exhust(pk=1, job_id='exhust_job_id', status=False)
				e.save()
				# time.sleep(5)
		if humidity <= humidity_nagitive:
			scheduler.print_jobs()
			try:
				e = Exhust.objects.get(pk=2)
				e.job_id='humidifer_job_id'
				e.status=True
				e.save()
				scheduler.resume_job('humidifer_job_id')
				# time.sleep(5)
			except Exception as e:
				e = Exhust(pk=2, job_id='humidifer_job_id', status=True)
				e.save()
				# time.sleep(5)
		else:
			try:
				e = Exhust.objects.get(pk=2)
				e.job_id='humidifer_job_id'
				e.status=False
				e.save()
				scheduler.print_jobs()
				scheduler.pause_job('humidifer_job_id')
				# time.sleep(5)
			except Exception as e:
				e = Exhust(pk=2, job_id='humidifer_job_id', status=False)
				e.save()
				# time.sleep(5)

	else:
		print('Failed to retrieve data from humidity sensor.')
		# time.sleep(5)



scheduler.add_job(check_hum_temp, 'interval', seconds=5, id='humidity_temp_job_id', replace_existing=True)
scheduler.add_job(exhust_relay_job, 'interval', seconds=7, id='exhust_job_id', replace_existing=True)
scheduler.add_job(humidifer_relay_job, 'interval', seconds=7, id='humidifer_job_id', replace_existing=True)
scheduler.add_job(humidity_temperature_logs, 'interval', seconds=30, id='humidity_temperature_logs_job_id', replace_existing=True)
scheduler.start()
