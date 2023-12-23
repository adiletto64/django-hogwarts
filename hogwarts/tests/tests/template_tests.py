from django.views.generic import CreateView, UpdateView, ListView, DetailView
import factory

from hogwarts.magic_tests.template import (
    create_detail_test,
    create_list_test,
    create_create_test,
    create_update_test, gen_imports
)

from hogwarts.utils import code_strip

from .testcase_tests import Poster
from hogwarts.magic_tests.template import gen_tests


class PosterFactory(factory.django.DjangoModelFactory):
    title = factory.Faker("name")
    content = factory.Faker("text")

    class Meta:
        model = Poster




def test_detail_test_creation():
    class PosterDetailView(DetailView):
        model = Poster
        template_name = "hmm.html"

    url = "posters:detail"

    expected = """
    def test_poster_detail(self):
        poster = PosterFactory()

        response = self.client.get(reverse("posters:detail", args=[poster.pk]))

        self.assertEqual(response.status_code, 200)
    """

    assert code_strip(create_detail_test(PosterDetailView, PosterFactory, url)) == code_strip(expected)


def test_list_test_creation():
    class PosterListView(ListView):
        model = Poster
        template_name = "hmm.html"
        context_object_name = "posters"

    url = "posters:list"

    expected = """
    def test_poster_list(self):
        PosterFactory.create_batch(3)

        response = self.client.get(reverse("posters:list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posters"]), 3)
    """

    assert code_strip(create_list_test(PosterListView, PosterFactory, url)) == code_strip(expected)


def test_create_test_creation():
    class PosterCreateView(CreateView):
        model = Poster
        fields = ["title", "content"]
        success_url = "/"

    url = "posters:create"

    expected = """
    def test_poster_create(self):
        payload = {
            "title": "test",
            "content": "test",
        } 

        response = self.client.post(reverse("posters:create"), payload)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Poster.objects.exists())
    """

    assert code_strip(create_create_test(PosterCreateView, url)) == code_strip(expected)


def test_update_test_creation():
    class PosterUpdateView(UpdateView):
        model = Poster
        fields = ["title", "content"]
        success_url = "/"

    url = "posters:update"

    expected = """
    def test_poster_update(self):
        poster = PosterFactory()

        payload = {
            "title": "test",       
            "content": "test",
        }

        response = self.client.post(reverse("posters:update", args=[poster.pk]), payload)
        poster.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(poster.title, payload["title"])
    """

    assert code_strip(create_update_test(PosterUpdateView, PosterFactory, url)) == code_strip(expected)


def test_it_generates_imports():
    result = gen_imports("posts")

    expected = """
    from django.tests import TestCase
    from django.shortcuts import reverse

    from posts.models import Post
    from posts.factories import PostFactory
    """

    assert result == code_strip(expected)



def test_it_generates_tests():
    result = gen_tests("posts")

    expected = """
    from django.tests import TestCase
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
    """

    assert result == code_strip(expected)
