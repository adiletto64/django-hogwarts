from django import forms
from django.views.generic import CreateView, RedirectView

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
