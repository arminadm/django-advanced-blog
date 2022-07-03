from django.test import TestCase
from blog.models import Category, Post
from datetime import datetime
from accounts.models import User, Profile

class TestPostModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(email = 'test@testcase.com')
        self.profile = Profile.objects.create(
            user = self.user,
            first_name = 'testcase_first_name',
            last_name = 'testcase_last_name',
        )
        self.category = Category.objects.create(name='test_category')

    def test_create_new_post_model_with_valid_data(self):
        post = Post.objects.create(
            author = self.profile,
            title = 'this post created by test case',
            content = 'this is a content about that post which created by test case',
            status = True,
            category = self.category,
            published_date = datetime.now()
        )
        self.assertTrue(Post.objects.filter(pk=post.id).exists())
        self.assertEquals(post.title, 'this post created by test case')
    