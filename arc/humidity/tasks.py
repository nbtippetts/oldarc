from __future__ import absolute_import, unicode_literals
from arc.celery import app
from celery.decorators import periodic_task
from django.db import connection
from datetime import datetime, timedelta, date
from .models import HumidityTemp, HumidityTempValues
import gpiozero
import redis
from .hum_temp import get_humidity_temperature
from signal import pause

rdb = redis.Redis(host='localhost',port=6379,db=0)

@periodic_task(
    run_every=300,
    name="humidity.log_humidity_temp",
	queue='check_humidity_temp_queue',
	options={'queue': 'check_humidity_temp_queue'}
)
def log_humidity_temp():
	humidity, temperature = get_humidity_temperature()
	if humidity is not None and temperature is not None:
		print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
		humidity_temp_db = HumidityTemp(
			humidity=humidity,
			temp=temperature,
			created_at=datetime.now()
		)
		humidity_temp_db.save()
		return humidity, temperature
	else:
		return "Failed to retrieve data from humidity sensor, Retry"
	return "EXIT"

@periodic_task(
    run_every=20,
    name="humidity.check_humidity_temp",
	queue='check_humidity_temp_queue',
	options={'queue': 'check_humidity_temp_queue'}
)
def check_humidity_temp():
	if not rdb.exists('relay_key'):
		rdb.set("relay_key","OFF")

	data = HumidityTempValues.objects.get(pk=1)
	try:
		humidity, temperature = get_humidity_temperature()
		if humidity is not None and temperature is not None:
			print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
			if humidity >= data.humidity_value or temperature >= data.temp_value:
				queue = rdb.get("relay_key")
				if queue == b"ON":
					return 'Relay is ON so exit.'

				if queue == b"OFF":
					relay_stats.delay(True)
					rdb.set("relay_key","ON")
					return 'sent task to relay!'

				return 'Humidity/Temperature out of params values turning Relay ON'
			else:
				rdb.set("relay_key","OFF")
				queue = rdb.get("relay_key")
				if queue == b"OFF":
					relay_stats.delay(False)
					return 'Relay OFF'
		else:
			rdb.set("relay_key","OFF")
			return 'Unable to read humidity and temperature.'
	except Exception as e:
		rdb.set("relay_key","OFF")
		return f"ERROR: {e}"


@app.task(bind=True)
def relay_stats(self,status):
	relay = gpiozero.OutputDevice(18, active_high=False, initial_value=False)
	if status:
		relay.on()
	else:
		relay.off()
		return 'Relay OFF'
	pause()
	return 'END TASK'