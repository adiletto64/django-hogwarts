from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255)


class Product(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    cost = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
