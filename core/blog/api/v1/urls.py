from django.urls import path, include
from .views import PostList, PostDetail

app_name = 'api-v1'

urlpatterns = [
    # path('posts/', api_post_list, name='api-post-list'),
    # path('posts/<int:pk>/', api_post_detail, name='api-post-detail')
    path('posts/', PostList.as_view(), name='api-post-list'),
    path('posts/<int:pk>/', PostDetail.as_view(), name='api-post-detail'),
]
