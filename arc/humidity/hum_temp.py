import Adafruit_DHT
import gpiozero

def get_humidity_temperature():
	sensor = Adafruit_DHT.DHT11
	pin =17
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	print(humidity,temperature)
	if humidity is not None and temperature is not None:
		return humidity, temperature
	else:
		return 0.0, 0.0
