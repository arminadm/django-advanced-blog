from django.urls import path, include
from accounts.views import sendEmail, testing_cache_time_delay

app_name = "accounts"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("api-v1/", include("accounts.api.v1.urls")),
    path("api-v2/", include("djoser.urls")),
    path("api-v2/", include("djoser.urls.jwt")),
    path("send-email", sendEmail, name='test-send-email'),
    path("cache-test", testing_cache_time_delay , name='cache-test')
]
