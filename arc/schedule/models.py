from django.db import models
from django.utils import timezone
from datetime import datetime

class Schedule(models.Model):
	start = models.TimeField(blank=True, null=True)
	deration=models.TimeField(blank=True, null=True)
	finish=models.TimeField(blank=True, null=True)
	finish_date = models.DateTimeField(default=timezone.now)
	next_schedule = models.DateTimeField(default=timezone.now)
	start_date = models.DateTimeField(default=timezone.now)
	how_often = models.TimeField(blank=True, null=True)
	gpio_pin = models.IntegerField(default=0)


class Relay(models.Model):
	relay_state = models.CharField(max_length=225, default='False')
	task_id = models.CharField(max_length=225, default='False')
	relay_start = models.DateTimeField(default=timezone.now)
	relay_finish = models.DateTimeField(default=timezone.now)
	gpio_pin = models.IntegerField(default=0)

class Relay14(models.Model):
	relay_state = models.CharField(max_length=225, default='False')
	task_id = models.CharField(max_length=225, default='False')
	relay_start = models.DateTimeField(default=timezone.now)
	relay_finish = models.DateTimeField(default=timezone.now)
	gpio_pin = models.IntegerField(default=0)
	def __str__(self):
		return self.relay_status

class Relay15(models.Model):
	relay_state = models.CharField(max_length=225, default='False')
	task_id = models.CharField(max_length=225, default='False')
	relay_start = models.DateTimeField(default=timezone.now)
	relay_finish = models.DateTimeField(default=timezone.now)
	gpio_pin = models.IntegerField(default=0)
	def __str__(self):
		return self.relay_status