from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.views.generic.base import RedirectView
from blog.models import Post
from accounts.models import Profile
from django.utils import timezone
from blog.forms import CreateNewPost
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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

class DetailViewOfPost(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'detail.html'
    context_object_name = 'post'
    # login_url = '/yechizi/' #use for loginrequiredmixin
    # redirect_field_name = 'redirect_to' #use for loginrequiredmixin
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context  

class FormViewNewPost(LoginRequiredMixin, PermissionRequiredMixin, FormView):
    form_class = CreateNewPost
    template_name = 'createNewPostByFormView.html'
    success_url = '/blog/'

    permission_required = 'blog.add_post' #APP.ACTION_OBJECT - used for permissionRequiredMixin

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class CreateViewNewPost(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    #fields = "__all__" 
    # fields = ['title', 'content', 'status', 'category', 'published_date'] # you can use following commented code line instead of this
    form_class = CreateNewPost
    template_name = 'createNewPostByCreateView.html'
    success_url = '/blog/'

    permission_required = 'blog.add_post' #APP.ACTION_OBJECT - used for permissionRequiredMixin
    
    def form_valid(self, form):
        user = Profile.objects.get(user=self.request.user)
        form.instance.author = user
        return super().form_valid(form)
    
class UpdateViewToEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'status', 'category', 'published_date']
    template_name = 'edit_post.html'
    
    permission_required = 'blog.change_post' #APP.ACTION_OBJECT - used for permissionRequiredMixin

    # you can user get_success_url instead of using success_url so you can have access to self
    def get_success_url(self):
        return reverse('blog:detailViewOfPost', args=(self.object.pk,))

class DeleteViewToDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    success_url = '/blog'
    template_name = 'delete_confirmation.html'

    permission_required = 'blog.delete_post' #APP.ACTION_OBJECT - used for permissionRequiredMixin