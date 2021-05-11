from datetime import datetime, timedelta, time
from django import forms
from .models import Schedule
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
on_off_gpio = (
	(True, 'Start'),
	(False, 'Stop'),
)
select_gpio_pin = (
	(14, 'Lights'),
	(15, 'Water')
)
select_duration = (
	(timedelta(seconds=10), '00:00:10'),
	(timedelta(minutes=2), '00:02'),
	(timedelta(minutes=30), '00:30'),
	(timedelta(hours=1), '01:00'),
	(timedelta(hours=1, minutes=30), '01:30'),
	(timedelta(hours=2), '02:00'),
	(timedelta(hours=2, minutes=30), '02:30'),
)
select_how_often = (
	(timedelta(seconds=20), '00:00:20'),
	(timedelta(minutes=3), '00:03'),
	(timedelta(hours=3), '03:00'),
	(timedelta(hours=3, minutes=30), '03:30'),
	(timedelta(hours=4), '04:00'),
	(timedelta(hours=4, minutes=30), '04:30'),
	(timedelta(hours=5), '05:00'),
	(timedelta(hours=5, minutes=30), '05:30'),
	(timedelta(hours=6), '06:00'),
	(timedelta(hours=6, minutes=30), '06:30'),
	(timedelta(hours=7), '07:00'),
	(timedelta(hours=7, minutes=30), '07:30'),
	(timedelta(hours=8), '08:00'),
	(timedelta(hours=8, minutes=30), '08:30'),
	(timedelta(hours=9), '09:00'),
	(timedelta(hours=9, minutes=30), '09:30'),
	(timedelta(hours=10), '10:00'),
	(timedelta(hours=10, minutes=30), '10:30'),
	(timedelta(hours=11), '11:00'),
	(timedelta(hours=11, minutes=30), '11:30'),
	(timedelta(hours=12), '12:00'),
	(timedelta(hours=23), '24:00'),
	(timedelta(hours=30), '30:00'),
	(timedelta(hours=48), '48:00'),
)

class TimeInput(forms.TimeInput):
	input_type = 'time'


class ScheduleForm(forms.Form):
	start = forms.TimeField(
		widget=TimeInput
	)
	deration = forms.ChoiceField(
		choices=select_duration
	)
	how_often = forms.ChoiceField(
		choices=select_how_often
	)
	gpio_pin = forms.ChoiceField(
		choices=select_gpio_pin
	)
	class Meta:
		model = Schedule


