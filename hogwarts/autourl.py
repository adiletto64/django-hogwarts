import inspect
import re
from dataclasses import dataclass
from enum import Enum
from inspect import isclass
from typing import Optional, Type

from django.urls import path
from django.views import View
from django.views.generic import DeleteView, DetailView, UpdateView

base_class_names = [
    'View',
    'ListView',
    'CreateView',
    'FormView',
    'DetailView',
    'DeleteView',
    'UpdateView',
]

detail_names = [
    "Detail",
    "Update",
    "Delete"
]

actions = [
    "list",
    "create"
]


class ViewType(Enum):
    FUNCTION = 1
    CLASS = 2


def auto_urls(views_module, app_name: str):
    views = import_views(views_module)
    urlpatterns = []

    for view in views:
        urlpatterns.append(get_path(view, app_name))

    return urlpatterns


def import_views(views_module):
    members = inspect.getmembers(views_module, predicate=is_view)
    return [t[1] for t in members]


def is_view(obj):
    try:
        name = obj.__name__
    except AttributeError:
        return False

    ends_with_view = name.lower().endswith("view")
    not_base_class = name not in base_class_names

    return ends_with_view and not_base_class


def get_path(view, app_name: Optional[str] = None):
    view_type = ViewType.CLASS if isclass(view) else ViewType.FUNCTION

    metadata: Path = getattr(view, "auto_url_path", None)
    if metadata:
        path_name = metadata.path_name
        path_url = metadata.path_urls if metadata.path_urls else get_path_url(path_name, detail=metadata.detail)

    else:
        path_name = get_path_name(view, app_name)
        path_url = get_path_url(path_name, detail=view_is_detail(view))

    if view_type == ViewType.CLASS:
        return path(path_url, view.as_view(), name=path_name)
    else:
        return path(path_url, view, name=path_name)


@dataclass
class Path:
    path_name: str
    detail: bool
    path_urls: Optional[str]


def auto_path(path_name: str,  path_url: Optional[str] = None, detail: bool = False):
    def wrapper(obj):
        obj.auto_url_path = Path(path_name, detail, path_url)
        return obj

    return wrapper


def get_path_name(view, app_name: Optional[str] = None):
    name: str = view.__name__
    view_type = ViewType.CLASS if isclass(view) else ViewType.FUNCTION

    if app_name:
        if view_type == ViewType.CLASS:
            app_name = app_name.capitalize()

        if app_name in name:
            name = name.replace(app_name, '')

        elif app_name.endswith('s'):
            if app_name in name:
                name = name.replace(app_name, '')
            if app_name[:-1] in name:
                name = name.replace(app_name[:-1], '')

    name = name.replace('View', '').replace('view', '')
    name = name.strip("_")

    return camel_to_snake(name)


def view_is_detail(view_class: Type[View]):
    for cls in [DeleteView, DetailView, UpdateView]:
        if issubclass(view_class, cls):
            return True

    return any(ending in view_class.__name__ for ending in detail_names)


def get_path_url(path_name: str, detail=False):
    if not detail and path_name == "list":
        return ""

    path_url = path_name.replace("_", "-") + "/"
    if detail:
        path_url = "<int:pk>/" + path_url

    return path_url


def camel_to_snake(camel_case_string):
    snake_case_string = re.sub(r'(?<=[a-z])([A-Z])', r'_\1', camel_case_string)
    snake_case_string = snake_case_string.lower()
    return snake_case_string
