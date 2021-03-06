from django.urls import path

from ..views import (
    RegistrationApiView,
    CustomAuthToken,
    DestroyAuthToken,
    CustomTokenObtainPairView,
    ChangePasswordApiView,
    TestActivateProfileView,
    ConfirmVerifyView,
    ResendVerifyView,
)

# from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # """registration and changes on account"""
    path("registration/", RegistrationApiView.as_view(), name="registration"),
    path(
        "change-password/",
        ChangePasswordApiView.as_view(),
        name="change-password",
    ),
    # """verification"""
    # after registration, token that is required for confirm-verification will be generated and sent to user email
    path(
        "test-verification/",
        TestActivateProfileView.as_view(),
        name="test-verification",
    ),
    path(
        "confirm-verification/<str:token>/",
        ConfirmVerifyView.as_view(),
        name="confirm-verification",
    ),
    # in case that previous token is expired or not valid anymore, user can get new token by it's email
    path(
        "resend-confirm-verification/",
        ResendVerifyView.as_view(),
        name="resend-confirm-verification",
    ),
    # """token"""
    # path('login/', ObtainAuthToken.as_view(), name='api-login'), #default token-login
    path("token/login/", CustomAuthToken.as_view(), name="login-token"),
    path("token/logout/", DestroyAuthToken.as_view(), name="logout-token"),
    # """jwt"""
    path(
        "jwt/create", CustomTokenObtainPairView.as_view(), name="create-jwt"
    ),
    path("jwt/refresh", TokenRefreshView.as_view(), name="refresh-jwt"),
    path("jwt/verify", TokenVerifyView.as_view(), name="verify-jwt"),
]
