from django.shortcuts import reverse
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


class PostCreateView(CreateView):
    model = Post
    fields = ["id", "title", "tags", "content"]
    template_name = "posts/post_create.html"

    def get_success_url(self):
        return reverse("posts:detail", args=[self.object.id])


class PostUpdateView(UpdateView):
    model = Post
    fields = ["id", "title", "tags", "content"]
    template_name = "posts/post_update.html"

    def get_success_url(self):
        return reverse("posts:detail", args=[self.get_object().id])
