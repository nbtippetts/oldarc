from django.db import models
from django.utils import timezone

class Water(models.Model):
	water_start = models.DateTimeField(default=timezone.now)
	water_deration=models.DateTimeField(default=timezone.now)
	how_often=models.IntegerField(default=0)
	water_finish=models.DateTimeField(default=timezone.now)
	next_water=models.DateTimeField(default=timezone.now)
