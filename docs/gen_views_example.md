# View generator example

command:
```shell
python manage.py genviews posts Post --smart-mode
```

model:
``` python
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```


result:
``` python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["id", "title", "content", "created_at"]
    template_name = "posts/post_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("posts:detail", args=[self.object.id])


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["id", "title", "content", "created_at"]
    template_name = "posts/post_update.html"

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse("posts:detail", args=[self.get_object().id])

```
