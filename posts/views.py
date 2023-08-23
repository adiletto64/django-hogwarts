from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from .models import Post, Comment


class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "posts/post_detail.html"


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ["id", "title", "tags", "content"]
    template_name = "posts/post_update.html"

    def get_success_url(self):
        return reverse("posts:detail", args=[self.get_object().id])


class CommentUpdateView(UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ["id", "post", "text"]
    template_name = "comments/comment_update.html"

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse("comments:detail", args=[self.get_object().id])


class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "posts/post_list.html"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["id", "title", "tags", "content"]
    template_name = "posts/post_create.html"

    def get_success_url(self):
        return reverse("posts:detail", args=[self.object.id])


class CommentDetailView(DetailView):
    model = Comment
    context_object_name = "comment"
    template_name = "comments/comment_detail.html"


class CommentListView(ListView):
    model = Comment
    context_object_name = "comments"
    template_name = "comments/comment_list.html"


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["id", "post", "text"]
    template_name = "comments/comment_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("comments:detail", args=[self.object.id])
