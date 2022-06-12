from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from blog.models import Post
# Create your views here.

#Function Based Views
'''
def indexFBView(request):
    context = {
        'name': 'name of user'
    }
    return render(request, 'index.html', context)
'''

class IndexCBView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all()
        context['name'] = 'name of user'
        context['post'] = posts
        return context

class RedirectToMaktab(RedirectView):
    permanent = False
    query_string = False
    url = 'https://maktabkhooneh.com'
    def get_redirect_url(self, **kwargs):
        posts = get_object_or_404(Post, pk=kwargs['pk'])
        print(posts)
        return super().get_redirect_url(**kwargs)
