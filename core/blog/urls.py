from django.urls import path
from blog.views import IndexCBView, RedirectToMaktab, ListViewOfPosts, DetailViewOfPost

app_name = 'blog'

urlpatterns = [
    path('', ListViewOfPosts.as_view(), name='listViewOfPosts'),
    path('<int:pk>/', DetailViewOfPost.as_view(), name='detailViewOfPost'),
    path('CBVindex', IndexCBView.as_view(), name='FBVindex'),
    path('go-to-maktab/<int:pk>', RedirectToMaktab.as_view(), name='maktab')
]
