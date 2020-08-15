from django import template
register = template.Library()
from ..models import Water

@register.inclusion_tag('water/latest_water.html')
def show_latest_water():
	latest_waters = Water.objects.all().order_by('-water_finish')[:1]
	return {'latest_waters': latest_waters}
