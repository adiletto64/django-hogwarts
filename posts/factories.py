import factory

from .models import Post, Comment


class PostFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("name")
    tags = factory.Faker("name")
    content = factory.Faker("paragraph")
    created_at = factory.Faker("date_time")

    class Meta:
        model = Post


class CommentFactory(factory.django.DjangoModelFactory):
    text = factory.Faker("name")

    class Meta:
        model = Comment
