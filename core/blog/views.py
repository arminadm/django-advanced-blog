from django.shortcuts import render
from django.views.generic import TemplateView
from blog.models import Post
# Create your views here.

#Function Based Views
def indexFBView(request):
    context = {
        'name': 'name of user'
    }
    return render(request, 'index.html', context)

class IndexCBView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = Post.objects.all()
        context['name'] = 'name of user'
        context['post'] = posts
        return context