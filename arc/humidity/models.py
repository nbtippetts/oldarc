from django.db import models
from django.utils import timezone


class HumidityTemp(models.Model):
	humidity = models.DecimalField(max_digits=6, decimal_places=2)
	temp = models.DecimalField(max_digits=6, decimal_places=2)
	created_at = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.humidity, self.temp
