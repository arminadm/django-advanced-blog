# from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from ...models import Post
from .serializer import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import GenericAPIView, mixins
from rest_framework.generics import ListAPIView, ListCreateAPIView

#STEP1: previous function based methods
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

#STEP2: using APIView for class based views
'''
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
'''

#STEP3: using GenericAPIView alone 
'''
class PostList(GenericAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

    def get(self, request):
        instance = self.get_queryset()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
'''


#STEP4: using GenericAPIView and mixins
'''
class PostList(GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

    # ??? UNSOLVED PROBLEM: where does get post or any other methods come from? why should i create these methods and why they are working?? ???
    # we have to make get method so we can connect GenericAPIView and mixins.ListModelMixin
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # we have to make post method so we can connect GenericAPIView and minixs.CreateModelMinixs
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
'''

#STEP5: using ListCreateAPIView
class PostList(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

class PostDetail(GenericAPIView):
    pass