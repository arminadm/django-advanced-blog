from rest_framework import serializers
from ...models import Post, Category

class PostSerializer(serializers.ModelSerializer):
    # content = serializers.ReadOnlyField() #first way to make specific filed to readonly
    # content = serializers.CharField(read_only=True) # second way to make specific filed to readonly
    snippet = serializers.ReadOnlyField(source='get_snippet')
    relative_url = serializers.URLField(source='get_absolute_api_url', read_only=True)
    absolute_url = serializers.SerializerMethodField(method_name='get_absolute_url') #the name default of function has to be get_ + name of variable, but if you wanted to name function
    #anything else, you can use method_name to solve your problem
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'snippet', 'status', 'category', 'relative_url', 'absolute_url', 'created_date', 'updated_date', 'published_date']
        # read_only_fields = ['content'] # third way to make specific filed to readonly

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'