from rest_framework import serializers
from ...models import Post, Category

class PostSerializer(serializers.ModelSerializer):
    content = serializers.ReadOnlyField() #first way to make specific filed to readonly
    # content = serializers.CharField(read_only=True) # second way to make specific filed to readonly
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'status', 'category', 'created_date', 'updated_date', 'published_date']
        # read_only_fields = ['content'] # third way to make specific filed to readonly

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'