from django.shortcuts import reverse
from django import forms
from django.views.generic import CreateView, RedirectView, DetailView, ListView, UpdateView
from .models import Post


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]


class ArticleCreateView(CreateView):
    form_class = ArticleForm
    template_name = "form.html"
    success_url = "/"


class MyRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return "/"


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
    fields = ["title", "tags", "content"]
    template_name = "posts/post_create.html"

    def get_success_url(self):
        return reverse("posts:detail", args=[self.object.id])


class PostUpdateView(UpdateView):
    model = Post
    fields = ["title", "tags", "content"]
    template_name = "posts/post_update.html"

    def get_success_url(self):
        return reverse("posts:detail", args=[self.get_object().id])
