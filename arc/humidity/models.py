from django.db import models
from django.utils import timezone


class HumidityTemp(models.Model):
	humidity = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
	temp = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
	created_at = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.humidity, self.temp

class HumidityTempValues(models.Model):
	humidity_value = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
	temp_value = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
	created_at = models.DateTimeField(default=timezone.now)
