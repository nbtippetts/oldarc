from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


jobstores = {
  'schedule_store': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@db:5432/arc_db')
# 'schedule_store': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@localhost:5432/arc_db')
}
executors = {
  'schedule_store': ThreadPoolExecutor(10),
  'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
  'coalesce': False,
  'max_instances': 25
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)

class ScheduleConfig(AppConfig):
    name = 'schedule'
    def ready(self):
    	scheduler.add_job(relay_14,'interval',seconds=5,id='button_relay_job_id_14', max_instances=1, replace_existing=True)
        scheduler.add_job(relay_15,'interval',seconds=4,id='button_relay_job_id_15', max_instances=1, replace_existing=True)
        scheduler.start()
