from django.db import models


# Create your models here.
class Example(models.Model):
    message = models.CharField(max_length=255)


class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    beta = models.BooleanField(default=False)

    