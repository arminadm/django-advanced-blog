from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ...models import Post
from .serializer import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def api_post_list(request):
    if request.method == 'GET':
        post = Post.objects.filter(status=True)
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def api_post_detail(request, pk):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=pk, status=True)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        post = get_object_or_404(Post, id=pk, status=True)
        serializer = PostSerializer(post, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data)
    elif request.method == 'DELETE':
        post = get_object_or_404(Post, id=pk, status=True)
        post.delete()
        return Response({"detail": "post removed successfully"})
