from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


jobstores = {
  'default': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@db:5432/arc_db')
#   'default': SQLAlchemyJobStore(url='postgresql+psycopg2://pi:rnautomations@localhost:5432/arc_db')
}
executors = {
  'default': ThreadPoolExecutor(10),
  'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
  'coalesce': False,
  'max_instances': 25
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)



class HumidityConfig(AppConfig):
    name = 'humidity'
    def ready(self):
        scheduler.add_job(check_hum_temp, 'interval', seconds=5, id='humidity_temp_job_id', max_instances=5, replace_existing=True)
        scheduler.add_job(check_hum, 'interval', seconds=4, id='check_humidity_job_id', max_instances=5, replace_existing=True)
        scheduler.add_job(exhaust_relay_job, 'interval', seconds=9, id='exhaust_job_id', max_instances=1, replace_existing=True)
        scheduler.add_job(humidifer_relay_job, 'interval', seconds=9, id='humidifer_job_id', max_instances=1, replace_existing=True)
        scheduler.add_job(humidity_temperature_logs, 'interval', seconds=30, id='humidity_temperature_logs_job_id', max_instances=1, replace_existing=True)
        # scheduler.add_job(humidity_temperature_logs, 'interval', seconds=900, id='humidity_temperature_logs_job_id', max_instances=1, replace_existing=True)
        scheduler.start()