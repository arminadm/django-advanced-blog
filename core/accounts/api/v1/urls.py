from django.urls import path, include
from .views import RegistrationApiView, CustomAuthToken
# from rest_framework.authtoken.views import ObtainAuthToken

app_name = 'api-v1'

urlpatterns = [
    # registration
    path('registration/', RegistrationApiView.as_view(), name='registration'),
    # path('login/', ObtainAuthToken.as_view(), name='api-login'), #default token-login
    path('login/', CustomAuthToken.as_view(), name='api-login'),
]
