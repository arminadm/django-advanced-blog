from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
# getting user model object
User = get_user_model()

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    content = models.TextField()
    status = models.BooleanField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField()
    
    def get_snippet(self):
        return self.content[0:8]
    
    def get_absolute_api_url(self): #changed the name from get_absolute_url to get_absolute_api_url so we dont get any conflict (it can be named anything)
        return reverse("blog:api-v1:post-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name