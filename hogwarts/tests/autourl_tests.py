from django.test import TestCase
from django.urls import path
from django.views import View

from .. import _test_views
from .._test_views import MyFormView, MyListView, get_view, post_view, confirm_post_view
from ..autourl import (
    auto_path,
    get_path,
    get_path_name,
    import_views,
)


class ProductCreateView(View): pass
class ProductsListView(View): pass
class ProductDetailView(View): pass
class SendMessageView(View): pass
class ConfirmOrderView(View): pass
def product_update_view(): pass
def dumb_files_view(): pass


class AutoUrlTestCase(TestCase):
    def test_it_imports_user_defined_views(self):
        imported_classes = import_views(_test_views)
        expected = [MyFormView, MyListView, confirm_post_view, get_view, post_view]

        self.assertListEqual(imported_classes, expected)

    def test_crud_get_path_name(self):
        payload = [
            (ProductCreateView, 'create'),
            (ProductsListView, 'list'),
            (ProductDetailView, 'detail'),
            (product_update_view, 'update')
        ]

        for view, expected_path_name in payload:
            path_name = get_path_name(view, 'products')
            self.assertEqual(path_name, expected_path_name)

    def test_get_path_name(self):
        payload = [
            (SendMessageView, "send_message"),
            (ConfirmOrderView, "confirm_order"),
            (dumb_files_view, "dumb_files")
        ]

        for view, expected_path_name in payload:
            path_name = get_path_name(view)
            self.assertEqual(path_name, expected_path_name)

    def test_auto_path_decorator(self):
        @auto_path("confirm", detail=True)
        class Some(View):
            pass

        expected_path = path("<int:pk>/confirm/", Some.as_view(), name="confirm")
        current_path = get_path(Some)

        self.assertPathEqual(expected_path, current_path)

    def test_decorator_custom_url(self):
        path_url = "<int:pk>/products"

        @auto_path("confirm", detail=True, path_url=path_url)
        class Another(View):
            pass

        expected_path = path(path_url, Another.as_view(), name="confirm")
        current_path = get_path(Another)

        self.assertPathEqual(expected_path, current_path)

    def assertPathEqual(self, path1, path2):
        self.assertEqual(path1.name, path2.name)
        self.assertEqual(path1.pattern.regex, path2.pattern.regex)
