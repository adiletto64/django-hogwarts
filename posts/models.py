from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    tags = models.CharField(max_length=255, help_text="write hashtags seperated by comma")
    content = models.TextField(help_text="You can use markdown!")
    created_at = models.DateTimeField(auto_now_add=True)
