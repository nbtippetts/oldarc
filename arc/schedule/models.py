from django.db import models
from django.utils import timezone

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

class Relay(models.Model):
	relay_state = models.CharField(max_length=225, default='False')
	task_id = models.CharField(max_length=225, default='False')
	relay_start = models.DateTimeField(default=timezone.now)
	relay_finish = models.DateTimeField(default=timezone.now)
	gpio_pin = models.IntegerField(default=0)

class Relay14(models.Model):
	relay_state = models.CharField(max_length=225, default='False')
	relay_start = models.DateTimeField(default=timezone.now)
	relay_finish = models.DateTimeField(default=timezone.now)
	gpio_pin = models.IntegerField(default=0)
	def __str__(self):
		return self.relay_status

class Relay15(models.Model):
	relay_state = models.CharField(max_length=225, default='False')
	relay_start = models.DateTimeField(default=timezone.now)
	relay_finish = models.DateTimeField(default=timezone.now)
	gpio_pin = models.IntegerField(default=0)
	def __str__(self):
		return self.relay_status