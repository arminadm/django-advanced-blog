from django.urls import path
from blog.views import FormViewNewPost, IndexCBView, RedirectToMaktab, ListViewOfPosts, DetailViewOfPost, FormViewNewPost, CreateViewNewPost, UpdateViewToEdit

app_name = 'blog'

urlpatterns = [
    path('', ListViewOfPosts.as_view(), name='listViewOfPosts'),
    path('<int:pk>/', DetailViewOfPost.as_view(), name='detailViewOfPost'),
    path('create_post-FV', FormViewNewPost.as_view(), name='formViewNewPost'),
    path('create_post-CV', CreateViewNewPost.as_view(), name='createViewNewPost'),
    path('<int:pk>/edit', UpdateViewToEdit.as_view(), name='updateViewToEdit'),
    path('CBVindex', IndexCBView.as_view(), name='FBVindex'),
    path('go-to-maktab/<int:pk>', RedirectToMaktab.as_view(), name='maktab')
]
