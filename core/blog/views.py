from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView
from django.views.generic.base import RedirectView
from blog.models import Post
from django.utils import timezone
from blog.forms import CreateNewPost
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
        context['name'] = self.request.user
        return context

class RedirectToMaktab(RedirectView):
    permanent = False
    query_string = False
    url = 'https://maktabkhooneh.com'
    def get_redirect_url(self, **kwargs):
        posts = get_object_or_404(Post, pk=kwargs['pk'])
        print(posts)
        return super().get_redirect_url(**kwargs)

class ListViewOfPosts(ListView):
    # model = Post
    queryset = Post.objects.filter(status=1)
    # def get_queryset(self):
    #   posts = Post.objects.filter(status=1)
    #   return posts 
    paginate_by = 5
    ordering = '-created_date'
    template_name = 'posts.html'
    context_object_name = 'posts'

class DetailViewOfPost(DetailView):
    model = Post
    template_name = 'detail.html'
    context_object_name = 'post'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context  

class FormViewNewPost(FormView):
    form_class = CreateNewPost
    template_name = 'createNewPostByFormView.html'
    success_url = '/blog/'
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class CreateViewNewPost(CreateView):
    model = Post
    #fields = "__all__" 
    fields = ['title', 'content', 'status', 'category', 'published_date'] # you can use following commented code line instead of this
    # form_class = CreateNewPost
    template_name = 'createNewPostByCreateView.html'
    success_url = '/blog/'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)