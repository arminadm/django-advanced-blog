from django import forms
from blog.models import Post

class CreateNewPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'category', 'published_date']