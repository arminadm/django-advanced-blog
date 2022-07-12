from django.http import HttpResponse
from time import sleep
from accounts.tasks import send_email

# Create your views here.
def sendEmail(request):
    # sleep(3)
    send_email.delay()
    return HttpResponse('<h1>Email send successfully</h1>')