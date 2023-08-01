from .. import views
from ..magic_urls.utils import extract_views


def test_views_extract():
    expected = [
        views.ExampleListView,
        views.ExampleCreateView,
        views.AddEqualSignView,
        views.ExampleDetailView
    ]

    result = extract_views(views)

    assert lists_equals(result, expected)


def lists_equals(arr1, arr2):
    return frozenset(arr1) == frozenset(arr2)
