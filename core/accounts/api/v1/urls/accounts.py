from django.urls import path
from ..views import (
    RegistrationApiView,
    CustomAuthToken,
    DestroyAuthToken,
    CustomTokenObtainPairView,
    ChangePasswordApiView,)
# from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # """registration"""
    path('registration/', RegistrationApiView.as_view(), name='registration'),
    
    # """change password"""
    path('change-password/', ChangePasswordApiView.as_view(), name='change-password'),

    # """set password"""

    # """login token"""
    # path('login/', ObtainAuthToken.as_view(), name='api-login'), #default token-login
    path('token/login/', CustomAuthToken.as_view(), name='login-token'),
    path('token/logout/', DestroyAuthToken.as_view(), name='logout-token'),

    # """login jwt"""
    path('jwt/create', CustomTokenObtainPairView.as_view(), name='create-jwt'),
    path('jwt/refresh', TokenRefreshView.as_view(), name='refresh-jwt'),
    path('jwt/verify', TokenVerifyView.as_view(), name='verify-jwt'),
]
