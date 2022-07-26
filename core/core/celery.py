from curses import panel
import os
from celery import Celery
from accounts.tasks import send_email

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

"""way no.2"""
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(10.0, send_email.s(), name='send email every 10 seconds')

"""how to use celery scheduling"""
# for scheduling the tasks we can use 3 different method:
#     1- add celery_beat_schedule into core.setting:
#         CELERY_BEAT_SCHEDULE = {
#             "sample_task": {
#                 "task": "core.tasks.sample_task",
#                 "schedule": crontab(minute="*/1"),
#             },
#         }
#    *Important Note: 
#     # we have to use following command so scheduling tasks work:
#     "$ celery -A core beat -l info"
#     ===============================================
#     2- add periodic task config to celery.py:
#         @app.on_after_configure.connect
#         def setup_periodic_tasks(sender, **kwargs):
#            sender.add_periodic_task(10.0, send_email.s(), name='send email every 10 seconds')
#    *Important Note: 
#     # we have to use following command so scheduling tasks work:
#     "$ celery -A core beat -l info"
#     ===============================================
#     3- use django-celery-beat module and manage scheduling by django admin panel
#     *Important Note:
#     we have to use following command so scheduling module works properly:
#     "$ celery -A core beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler"