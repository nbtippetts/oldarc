from celery import shared_task, app


@shared_task
def adding_task(x, y):
    return x + y

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
