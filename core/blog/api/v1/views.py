# from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from ...models import Post
from .serializer import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.views import APIView
from rest_framework import status

# previous function based methods
"""
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
"""

class PostList(APIView):
    """ displaying all the posts with true status and allow logged in users to save new posts """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def get(self, request):
        """ getting the data of all the posts with true status """
        posts = Post.objects.filter(status=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ creating new post for users who logged in """
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PostDetail(APIView):
    """ showing the detail of each post to admin user (others can't see) and also allow admin to change or delete """
    permission_classes = [IsAdminUser]
    serializer_class = PostSerializer
    
    def get(self, request, pk):
        """ showing the detail of each single post via it's pk (only admin can see) """
        post = get_object_or_404(Post, status=True, id=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        """ changing the detail of each single post via it's pk (only admin can change) """
        post = get_object_or_404(Post, status=True, id=pk)
        serializer = PostSerializer(post, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        """ delete each post via it's pk (only admin can delete) """
        post = get_object_or_404(Post, status=True, id=pk)
        post.delete()
        return Response({"detail":"Post object removed successfully"}, status=status.HTTP_204_NO_CONTENT)