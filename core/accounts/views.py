from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from time import sleep
from accounts.tasks import send_email
from requests import get

# Create your views here.
def sendEmail(request):
    # sleep(3)
    send_email.delay()
    return HttpResponse("<h1>Email send successfully</h1>")

# cache info for 15 seconds
@cache_page(15)
def testing_cache_time_delay(request):
    response = get("https://65cbad3d-952d-4f60-91f9-4f9a722f56ce.mock.pstmn.io/test/delay_5s")    
    return JsonResponse(response.json())
