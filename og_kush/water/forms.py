import datetime

from django import forms
from .models import Water
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class WaterForm(forms.Form):
	water_start=forms.DateField(help_text="Start Water")
	water_deration=forms.DateField(help_text="How Long")
	how_often=forms.DateField(help_text="How Often")

	def set_water_time(self):
		water_start = self.cleaned_data['water_start']
		water_deration = self.cleaned_data['water_deration']
		how_often = self.cleaned_data['how_often']

		# Check if a date is not in the past.
		if water_start < datetime.date.today():
			raise ValidationError(_('Invalid date - Can\'t water in the past'))

		# Remember to always return the cleaned data.
		return water_start, water_deration, how_often
