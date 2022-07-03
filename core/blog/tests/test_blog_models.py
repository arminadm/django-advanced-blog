from django.test import TestCase
from blog.models import Category, Post
from datetime import datetime
from accounts.models import User, Profile

class TestPostModel(TestCase):
    def test_create_new_post_model(self):
        user = User.objects.create(email = 'test@testcase.com')
        profile = Profile.objects.create(
            user = user,
            first_name = 'testcase_first_name',
            last_name = 'testcase_last_name',
        )
        category = Category.objects.create(name='test_category')
        post = Post.objects.create(
            author = profile,
            title = 'this post created by test case',
            content = 'this is a content about that post which created by test case',
            status = True,
            category = category,
            published_date = datetime.now()
        )
        self.assertEquals(post.title, 'this post created by test case')