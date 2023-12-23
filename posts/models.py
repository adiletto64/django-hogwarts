from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="название")
    tags = models.CharField(max_length=255, help_text="write hashtags seperated by comma", verbose_name="теги")
    content = models.TextField(help_text="You can use markdown!", verbose_name="контент")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="создан")

    class Meta:
        verbose_name = "Пост"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
