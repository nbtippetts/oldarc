from datetime import datetime, timedelta, time
from django import forms
from .models import Water, WaterPump
from django_celery_beat.models import PeriodicTasks, PeriodicTask, IntervalSchedule
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

select_gpio_pin = (
	(14, 'pin14 - Relay 1'),
	(15, 'pin15 - Relay 2'),
	(18, 'pin18 - Relay 3'),
	(23, 'pin23 - Relay 4'),
	(24, 'pin24 - Relay 5'),
	(25, 'pin25 - Relay 6'),
	(8, 'pin8 - Relay 7'),
	# (7, 'pin7 - Relay 8'),
)
select_duration = (
	(timedelta(minutes=30), '00:30'),
	(timedelta(hours=1), '01:00'),
	(timedelta(hours=1, minutes=30), '01:30'),
	(timedelta(hours=2), '02:00'),
	(timedelta(hours=2, minutes=30), '02:30'),
)
select_how_often = (
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

class DateInput(forms.DateInput):
	input_type = 'date'
class TimeInput(forms.TimeInput):
	input_type = 'time'


class WaterForm(forms.Form):
	water_start_date = forms.DateField(
		widget=DateInput
	)
	water_start = forms.TimeField(
		widget=TimeInput
	)
	water_deration = forms.ChoiceField(
		choices=select_duration
	)
	how_often = forms.ChoiceField(
		choices=select_how_often
	)
	gpio_pin = forms.ChoiceField(
		choices=select_gpio_pin
	)
	name = forms.CharField()
	task_name = forms.CharField()

	def water_time(self):
		water_start_date = self.cleaned_data['water_start_date']
		water_start = self.cleaned_data['water_start']
		water_deration = self.cleaned_data['water_deration']
		how_often = self.cleaned_data['how_often']

		water_deration = datetime.strptime(water_deration, '%H:%M:%S')
		how_often = datetime.strptime(how_often, '%H:%M:%S')
		return how_often, water_deration


class WaterPumpForm(forms.Form):
	pump_status = forms.CharField()
	gpio_pin = forms.ChoiceField(
		choices=select_gpio_pin
	)
	class Meta:
		model = WaterPump
	def set_status(self):
		pump_status = self.cleaned_data['pump_status']
		if pump_status != 'start' or pump_status != 'stop':
			raise ValidationError(_('Invalid data'))
		return pump_status
