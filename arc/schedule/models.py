from django.db import models
from django.utils import timezone


class WaterPump(models.Model):
	pump_status = models.CharField(max_length=225, default='False')
	pump_start = models.DateTimeField(default=timezone.now)
	pump_finish = models.DateTimeField(default=timezone.now)
	gpio_pin = models.IntegerField(default=0)
	def __str__(self):
		return self.pump_status


class Schedule(models.Model):
	start = models.TimeField(default=0)
	deration=models.TimeField(default=0)
	finish=models.TimeField(default=0)
	next_schedule = models.TimeField(default=0)
	start_date = models.DateField(default=0)
	how_often = models.TimeField(default=0)
	gpio_pin = models.IntegerField(default=0)
	# class Meta:
	# 	db_table = 	schedule'
