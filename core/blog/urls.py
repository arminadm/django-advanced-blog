from django.urls import path
from blog.views import IndexCBView, RedirectToMaktab, ListViewOfPosts

app_name = 'blog'

urlpatterns = [
    path('', ListViewOfPosts.as_view(), name='listViewOfPosts'),
    path('CBVindex', IndexCBView.as_view(), name='FBVindex'),
    path('go-to-maktab/<int:pk>', RedirectToMaktab.as_view(), name='maktab')
]
