from celery import shared_task
from time import sleep

@shared_task
def send_email():
    sleep(3)
    print('EMAIL SEND SUCCESSFULLY')

