from django.test import TestCase
from blog.forms import CreateNewPost
from blog.models import Category
from datetime import datetime

class TestForm(TestCase):
    def test_create_new_post_form_by_valid_data(self):
        category = Category.objects.create(name='test_category')
        form = CreateNewPost(data={
            "title":'this post created by test case',
            "content":'this is a content about that post which created by test case',
            "status":True,
            "category":category,
            "published_date":datetime.now()
        })
        self.assertTrue(form.is_valid())
    
    def test_create_new_post_form_by_no_data(self):
        form = CreateNewPost(data={})
        self.assertFalse(form.is_valid())