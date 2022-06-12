from django.urls import path
from blog.views import IndexCBView, RedirectToMaktab

urlpatterns = [
    path('CBVindex', IndexCBView.as_view(), name='FBVindex'),
    path('go-to-maktab/<int:pk>', RedirectToMaktab.as_view(), name='maktab')
]
