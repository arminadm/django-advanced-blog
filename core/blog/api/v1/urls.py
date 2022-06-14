from django.urls import path, include
from .views import api_post_detail, api_post_list

app_name = 'api-v1'

urlpatterns = [
    path('posts/', api_post_list, name='api-post-list'),
    path('posts/<int:pk>/', api_post_detail, name='api-post-detail')
]
