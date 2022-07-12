from celery import shared_task
from time import sleep

@shared_task
def send_email():
    sleep(3)
    print('EMAIL SEND SUCCESSFULLY')

# for scheduling the tasks we can use 3 different method:
#     1- add celery_beat_schedule into core.setting:
#         CELERY_BEAT_SCHEDULE = {
#             "sample_task": {
#                 "task": "core.tasks.sample_task",
#                 "schedule": crontab(minute="*/1"),
#             },
#         }
#     ===============================================
#     2- 