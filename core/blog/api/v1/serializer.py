from rest_framework import serializers
from ...models import Post, Category
from accounts.models import Profile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class PostSerializer(serializers.ModelSerializer):
    # content = serializers.ReadOnlyField() #first way to make specific filed to readonly
    # content = serializers.CharField(read_only=True) # second way to make specific filed to readonly
    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(
        source="get_absolute_api_url", read_only=True
    )
    absolute_url = serializers.SerializerMethodField(
        method_name="get_absolute_url"
    )  # the name default of function has to be get_ + name of variable, but if you wanted to name function
    # anything else, you can use method_name to solve your problem

    # category = serializers.SlugRelatedField(many=False, slug_field='name', queryset=Category.objects.all()) # way1: showing detail of category instead of id only
    # category = CategorySerializer() # way2: showing detail of category instead of id only

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "image",
            "content",
            "snippet",
            "status",
            "category",
            "relative_url",
            "absolute_url",
            "created_date",
            "updated_date",
            "published_date",
        ]
        # read_only_fields = ['content'] # third way to make specific filed to readonly
        read_only_fields = ["author"]

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)

    # when we want to separate what user can see with functionality, we can use to_representation
    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            """if we are representing single page"""
            rep.pop("snippet", None)
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)
        else:
            """if we are representing list page"""
            rep.pop("content", None)
            rep.pop("created_date", None)
            rep.pop("updated_date", None)

        rep["category"] = CategorySerializer(
            instance.category
        ).data  # way3: showing detail of category instead of id only
        return rep

    # we can override any method that serializer has, for example i want to override author with the current user, automatically and dont let user to change author him self
    def create(self, validated_data):
        request = self.context.get("request")
        current_user_id = request.user.id
        current_user_profile = Profile.objects.get(user_id=current_user_id)
        validated_data["author"] = current_user_profile
        return super().create(validated_data)
