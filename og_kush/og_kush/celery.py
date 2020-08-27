from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
# from celery import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'og_kush.settings')

app = Celery('og_kush')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'add-every-20-seconds': {
        'task': 'humidity.tasks.log_humidity_temp',
        'schedule': 20
    },
}
app.conf.timezone = 'UTC'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
