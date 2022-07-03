from urllib import response
from django.urls import reverse
from django.test import TestCase, Client
from accounts.models import User, Profile
from blog.models import Post, Category
from datetime import datetime

class TestBlogView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email = 'test@testcase.com')
        self.profile = Profile.objects.create(
            user = self.user,
            first_name = 'testcase_first_name',
            last_name = 'testcase_last_name',
        )
        self.category = Category.objects.create(name='test_category')
        self.post = Post.objects.create(
            author = self.profile,
            title = 'this post created by test case',
            content = 'this is a content about that post which created by test case',
            status = True,
            category = self.category,
            published_date = datetime.now()
        )

    def test_blog_post_lists_view(self):
        url = reverse('blog:listViewOfPosts')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(str(response.content).find('testing the put method via post man on this post'))
        self.assertTemplateUsed(response, 'posts.html')

    def test_blog_logged_in_user_detail_views(self):
        self.client.force_login(self.user)
        url = reverse('blog:detailViewOfPost', kwargs={'pk':self.post.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def test_blog_anonymous_user_detail_views(self):
        url = reverse('blog:detailViewOfPost', kwargs={'pk':self.post.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)