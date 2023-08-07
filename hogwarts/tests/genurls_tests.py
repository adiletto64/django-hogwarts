from ..magic_urls.gen_urls import gen_urlpatterns, gen_path, gen_url_imports
from ..magic_urls import custom_path

from .. import _test_views


def test_it_generates_path():
    result = gen_path(_test_views.MyListView, "my")
    expected = 'path("", MyListView.as_view(), name="list")'

    assert result == expected


def test_it_generates_path_for_function():
    result = gen_path(_test_views.confirm_post_view, "none")
    expected = 'path("confirm-post/", confirm_post_view, name="confirm_post")'

    assert result == expected


def test_it_extracts_metadata():
    @custom_path("green", "green-hello/")
    class RedView:
        pass

    result = gen_path(RedView, "none")
    expected = 'path("green-hello/", RedView.as_view(), name="green")'

    assert result == expected


def test_it_generates_urls():
    result = gen_urlpatterns(_test_views, "my")

    expected = """
urlpatterns = [
    path("form/", MyFormView.as_view(), name="form"),
    path("", MyListView.as_view(), name="list"),
    path("confirm-post/", confirm_post_view, name="confirm_post"),
    path("get/", get_view, name="get"),
    path("post/", post_view, name="post")
]    
    """

    assert result == expected


def test_it_generates_imports():
    result = gen_url_imports([
        _test_views.MyListView,
        _test_views.MyFormView,
        _test_views.get_view
    ], "_test_views")

    expected = """from ._test_views import MyListView, MyFormView, get_view"""

    assert result == expected
