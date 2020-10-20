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
app.control.purge()
rdb = redis.Redis(host='redis',port=6379,db=0)
#rdb = redis.Redis(host='localhost',port=6379,db=0)

@periodic_task(
    run_every=301,
    name="humidity.log_humidity_temp",
    queue="queue_humidity",
    options={"queue": "queue_humidity"},
	soft_time_limit=30
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
    queue="queue_humidity",
    options={"queue": "queue_humidity"},
	soft_time_limit=15
)
def check_humidity_temp():
	if not rdb.exists('relay_key'):
		rdb.set("relay_key","OFF")

	try:
		data = HumidityTempValues.objects.get(pk=1)
		print(data)
	except Exception as e:
		print('no data')
		h = HumidityTempValues(
			humidity_value=50.0,
			temp_value=50.0
		)
		h.save()
		data = HumidityTempValues.objects.get(pk=1)
		pass
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
					return 'Celery Relay OFF 1'
		else:
			rdb.set("relay_key","OFF")
			return 'Unable to read humidity and temperature.'
	except Exception as e:
		rdb.set("relay_key","OFF")
		return f"ERROR: {e}"


@app.task(bind=True,queue="queue_humidity",max_retry=0,ignore_results=True)
def relay_stats(self,status):
	relay = gpiozero.OutputDevice(18, active_high=False, initial_value=False)
	if status:
		relay.on()
		print("relay is now ON")
		pause()
	else:
		relay.off()
		print('Celery Relay OFF 2')
