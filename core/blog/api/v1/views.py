from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ...models import Post
from .serializer import PostSerializer

@api_view(['GET', 'POST'])
def api_post_list(request):
    if request.method == 'GET':
        post = Post.objects.filter(status=True)
        serializedPost = PostSerializer(post, many=True)
        return Response(serializedPost.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

@api_view()
def api_post_detail(request, pk):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=pk, status=True)
        serializedPost = PostSerializer(post)
        return Response(serializedPost.data)
        



