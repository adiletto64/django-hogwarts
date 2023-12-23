from django.db import models
from django.views.generic import CreateView, FormView

from hogwarts.magic_tests.testcase import import_app_endpoints, create_test_name, get_fields

from posts.factories import PostFactory


def test_it_finds_factory_for_endpoint():
    endpoints = import_app_endpoints('posts')

    for endpoint in endpoints:
        endpoint.find_factory('posts')
        assert endpoint.factory == PostFactory


def test_it_creates_test_name_from_view():
    assert create_test_name('ProductDetailView') == "test_product_detail"
    assert create_test_name("ConfirmMessageView") == "test_confirm_message"
    assert create_test_name("get_all_products_view") == "test_get_all_products"


class Poster(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()


def test_it_gets_fields_from_create_view():
    # get fields from fields attribute
    class PosterCreateView(CreateView): model = Poster; fields = ["title", "content"]
    assert get_fields(PosterCreateView) == list(Poster._meta.fields[1:])

    # get fields from form_class
    class PosterForm(FormView): model = Poster; fields = ["title", "content"]
    class PosterCreateView(CreateView): form_class = PosterForm

    assert get_fields(PosterCreateView) == list(Poster._meta.fields[1:])
