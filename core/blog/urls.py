from django.urls import path
from blog.views import indexFBView, IndexCBView

urlpatterns = [
    path('FBVindex', indexFBView, name='FBVindex'),
    path('CBVindex', IndexCBView.as_view(), name='FBVindex'),
]
