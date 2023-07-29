from ..autourl import gen_urls, gen_string_path

from .. import _test_views


def test_it_generates_path():
    result = gen_string_path(_test_views.MyListView, "my")
    expected = 'path("", MyListView.as_view(), name="list")'

    assert result == expected


def test_it_generates_path_for_function():
    result = gen_string_path(_test_views.confirm_post_view, "none")
    expected = 'path("confirm-post/", confirm_post_view, name="confirm_post")'

    assert result == expected


def test_it_generates_urls():
    result = gen_urls(_test_views, "my")

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

