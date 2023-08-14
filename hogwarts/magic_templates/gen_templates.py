import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type

import jinja2
from django.views import View
from django.conf import settings

from hogwarts.magic_urls._base import import_views
from hogwarts.magic_urls.utils import Path, extract_paths
from hogwarts.management.commands.base import get_views_module

GENERIC_VIEWS = ("CreateView", "UpdateView", "ListView", "DetailView")


class ViewType(Enum):
    CREATE = "CreateView"
    UPDATE = "UpdateView"
    DETAIL = "DetailView"
    LIST = "ListView"


@dataclass
class Endpoint:
    view: Type[View]
    template_name: str
    path_name: str
    view_type: Optional[ViewType]


def gen_templates(app_name: str):
    endpoints = get_endpoints(app_name)
    templates_dir = settings.TEMPLATES["DIRS"][0]

    for endpoint in endpoints:
        if endpoint.view_type == ViewType.CREATE:
            pass


def create_nested_file(templates_dir, new_template, content):
    full_path = os.path.join(templates_dir, new_template)

    dir_path, file_name = os.path.split(full_path)
    os.makedirs(dir_path, exist_ok=True)

    with open(full_path, 'w') as file:
        file.write(content)


def get_endpoints(app_name: str):
    views = get_views(app_name)
    paths = get_paths(app_name)

    endpoints: list[Endpoint] = []

    for view in views:
        endpoint = get_endpoint(view, paths, app_name)
        if endpoint.view_type:
            endpoints.append(endpoint)

    return endpoints

def get_views(app_name: str):
    views_module = get_views_module(app_name)
    return import_views(views_module)


def get_paths(app_name: str):
    urls_py = open(f"{app_name}\\urls.py", "r").read()
    return extract_paths(urls_py)


def get_endpoint(view, paths: list[Path], app_name: Optional[str]):
    path_name = find_path_name(view.__name__, paths)
    path_name = f"{app_name}:{path_name}" if app_name else path_name
    view_type = get_view_type(view.__name__)

    return Endpoint(view, view.template_name, path_name, view_type)


def find_path_name(view: str, paths: list[Path]):
    for path in paths:
        if path.view == view:
            return path.path_name


def get_view_type(view: str):
    if view.endswith(ViewType.CREATE.value):
        return ViewType.CREATE

    if view.endswith(ViewType.UPDATE.value):
        return ViewType.UPDATE

    if view.endswith(ViewType.DETAIL.value):
        return ViewType.DETAIL

    if view.endswith(ViewType.LIST.value):
        return ViewType.LIST
    else:
        return None
