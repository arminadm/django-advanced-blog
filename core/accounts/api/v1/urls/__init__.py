from django.urls import path, include

urlpatterns = [
    path("", include("accounts.api.v1.urls.accounts_url")),
    path("profile/", include("accounts.api.v1.urls.profile_url")),
]
