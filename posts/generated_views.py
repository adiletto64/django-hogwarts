from django.views.generic import DetailView, ListView, CreateView, UpdateView
from .models import Post

class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post_detail.html"

class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts/post_list.html"

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["id", "author", "title", "content", "created_at"]
    template_name = "posts/post_create.html"
    success_url = "/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["id", "author", "title", "content", "created_at"]
    template_name = "posts/post_update.html"
    success_url = "/"

    def test_func(self):
        return self.get_object() == self.request.user
