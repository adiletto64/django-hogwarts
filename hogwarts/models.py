from django.db import models


# Create your models here.
class Example(models.Model):
    message = models.CharField(max_length=255)
    