from django.urls import path, include
# from .views import PostList, PostDetail
from .views import PostViewSet
from rest_framework.routers import DefaultRouter

app_name = 'api-v1'

router = DefaultRouter()
router.register('post', PostViewSet, basename='post')
urlpatterns = router.urls


# urlpatterns = [
#     # path('posts/', api_post_list, name='api-post-list'),
#     # path('posts/<int:pk>/', api_post_detail, name='api-post-detail')
#     # path('posts/', PostList.as_view(), name='api-post-list'),
#     # path('posts/<int:pk>/', PostDetail.as_view(), name='api-post-detail'),
#     path('posts/', PostViewSet.as_view({'get':'list', 'post':'create'}), name='api-post-list'),
#     path('posts/<int:pk>/', PostViewSet.as_view({'get':'retrieve', 'put':'update', 'delete':'destroy'}), name='api-post-detail'),
# ]
