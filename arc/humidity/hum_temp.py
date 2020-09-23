import Adafruit_DHT
import gpiozero

def get_humidity_temperature():
	sensor = Adafruit_DHT.DHT11
	pin = 2
	try:
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		return humidity, temperature
	except Exception as e:
		return e