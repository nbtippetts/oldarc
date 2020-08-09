from django.db import models
from django.utils import timezone

class Water(models.Model):
	water_start = models.DateTimeField(default=timezone.now)
	water_deration=models.DateTimeField(default=timezone.now)
	how_often=models.IntegerField(default=0)
	water_finish=models.DateTimeField(default=timezone.now)
	next_water=models.DateTimeField(default=timezone.now)
	# class Meta:
	# 	db_table = 'water_schedule'

class WaterPump(models.Model):
	pump_status = models.CharField(max_length=225,default='stop')
	def __str__(self):
		return self.pump_status
