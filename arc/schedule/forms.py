from datetime import datetime, timedelta, time
from django import forms
from .models import Schedule,RelayStatus
from simpleduration import Duration
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
	duration_hours = forms.CharField(label='Duration',widget=forms.TextInput(attrs={'placeholder': 'Hours'}))
	duration_minutes = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Minutes'}))
	duration_seconds = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder': 'Seconds'}))
	how_often = forms.DurationField(widget=forms.TextInput(attrs={'placeholder': '24 Hour Format 00:00:00'}))
	gpio_pin = forms.ChoiceField(
		choices=select_gpio_pin
	)
	def clean(self):
		cleaned_data = super().clean()
		duration_hours = self.cleaned_data['duration_hours']
		duration_minutes = self.cleaned_data['duration_minutes']
		duration_seconds = self.cleaned_data['duration_seconds']
		self.cleaned_data['duration']=Duration(f'{duration_hours} hours {duration_minutes} minutes {duration_seconds} seconds')
		self.cleaned_data['duration']=self.cleaned_data['duration'].timedelta()
		how_often = self.cleaned_data['how_often']
		if self.cleaned_data['duration'].seconds >= how_often.seconds:
			# messages.error(request,"Duration must be less then how often")
			raise forms.ValidationError("Duration must be less then how often")
		# return self.cleaned_data
	class Meta:
		model = Schedule



class RelayStatusForm(forms.Form):
	# status = forms.ChoiceField(
	# 	label=False,
	# 	choices=on_off_gpio,
	# 	widget=forms.RadioSelect
	# )
	class Meta:
		model = RelayStatus
		fields = ('ON','OFF')
		widgets = {
			'ON': forms.TextInput(attrs={'class': 'form-control'}),
			'OFF': forms.TextInput(attrs={'class': 'form-control'})
		}