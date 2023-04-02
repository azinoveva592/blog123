from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic import ListView, DetailView # new
from django.views.generic.edit import CreateView, UpdateView, DeleteView  # new
from django.urls import reverse_lazy # new
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from .forms import CommentForm
from .models import Post
def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/templates/home.html',
                  {'page': page,
                   'posts': posts})

class PostDisplay(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

class PostComment(SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm
    template_name = 'post_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PostComment, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse('post_detail', kwargs={'pk': post.pk}) + '#comments'


class BlogListView(ListView):
    paginate_by = 3
    model = Post
    template_name = "home.html"
    context_object_name = 'posts'

class BlogDetailView(DetailView): # new
    model = Post
    template_name = "post_detail.html"
    context_object_name = 'post'

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.pk)])
    def get(self, request, *args, **kwargs):
        view = PostDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostComment.as_view()
        return view(request, *args, **kwargs)

class BlogCreateView(CreateView): # new
    model = Post
    template_name = "post_new.html"
    fields = ["title", "author", "body"]


class BlogUpdateView(UpdateView): # new
    model = Post
    template_name = "post_edit.html"
    fields = ["title", "body"]


class BlogDeleteView(DeleteView): # new
    model = Post
    template_name = "post_delete.html"
    success_url = reverse_lazy("home")
