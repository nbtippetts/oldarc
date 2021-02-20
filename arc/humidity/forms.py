from datetime import datetime, timedelta, time
from django import forms
from .models import HumidityTempValues
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class HumidityTempForm(forms.Form):
	humidity_value = forms.DecimalField(max_digits=6, decimal_places=2)
	buffer_value = forms.DecimalField(max_digits=6, decimal_places=2)
	temp_value = forms.DecimalField(max_digits=6, decimal_places=2)
	class Meta:
		model = HumidityTempValues
