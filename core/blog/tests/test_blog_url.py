from django.test import SimpleTestCase
from django.urls import reverse, resolve
from blog.views import ListViewOfPosts, DetailViewOfPost

# Create your tests here.
class TestURL(SimpleTestCase):
    def test_list_of_posts_url_resolve(self):
        url = reverse('blog:listViewOfPosts')
        self.assertEquals(resolve(url).func.view_class, ListViewOfPosts)
    
    def test_detail_of_post_url_resolve(self):
        url = reverse('blog:detailViewOfPost', kwargs={'pk':1})
        self.assertEquals(resolve(url).func.view_class, DetailViewOfPost)
        