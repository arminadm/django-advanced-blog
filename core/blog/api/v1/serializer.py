from rest_framework import serializers
from ...models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'status', 'category', 'created_date', 'updated_date', 'published_date']