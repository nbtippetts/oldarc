from django import template
register = template.Library()
from ..models import Schedule

@register.inclusion_tag('water/latest_schedule.html')
def show_latest_schedule():
	latest_schedule = Schedule.objects.all().order_by('-finish')[:1]
	return {'latest_schedule': latest_schedule}
