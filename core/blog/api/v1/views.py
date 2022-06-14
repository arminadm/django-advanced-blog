from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...models import Post
from .serializer import PostSerializer

@api_view()
def api_post_list(request):
    post = Post.objects.filter(status=True)
    serializedPost = PostSerializer(post, many=True)
    return Response(serializedPost.data)

@api_view()
def api_post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    serializedPost = PostSerializer(post)
    return Response(serializedPost.data)

