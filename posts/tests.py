from django.test import TestCase
from django.shortcuts import reverse

from posts.models import Post
from posts.factories import PostFactory


class PostTestCase(TestCase):
    def test_post_detail(self):
        post = PostFactory()

        response = self.client.get(reverse("posts:detail", args=[post.pk]))

        self.assertEqual(response.status_code, 200)

    def test_post_list(self):
        PostFactory.create_batch(3)

        response = self.client.get(reverse("posts:list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posts"]), 3)

    def test_post_create(self):
        payload = {
            "title": "test",
            "tags": "test",
            "content": "test",
        }

        response = self.client.post(reverse("posts:create"), payload)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.exists())

    def test_post_update(self):
        post = PostFactory()

        payload = {
            "title": "test",
            "tags": "test",
            "content": "test",
        }

        response = self.client.post(reverse("posts:update", args=[post.pk]), payload)
        post.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(post.title, payload["title"])
