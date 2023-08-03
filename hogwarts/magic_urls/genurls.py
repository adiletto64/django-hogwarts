import re
from inspect import isclass
from typing import Tuple, Optional

from hogwarts.magic_urls._base import (
    import_views,
    get_path_name,
    get_path_url,
    view_is_detail,
    has_path_decorator,
    get_decorator_path_name,
    get_decorator_path_url
)


def gen_urls_py(views_module, urls_path):
    imports = gen_url_imports(import_views(views_module), "views")
    urlpatterns = gen_urlpatterns(views_module, "example")

    with open(f"{urls_path}", 'w') as file:
        file.write(imports + "\n\n" + urlpatterns)


def merge_urls_py(views_module, urls_path):
    file = open(urls_path, "r")
    code = file.read()

    imports, urlpatterns = separate_imports_and_urlpatterns(code)
    app_name = get_app_name(code) or "example" # TODO fix this!
    views = import_views(views_module)
    paths = []

    for view in views:
        paths.append(gen_string_path(view, app_name))

    for view in views:
        if view.__name__ not in imports:
            imports = append_view_into_imports(imports, view)

    for path in paths:
        if path not in urlpatterns:
            urlpatterns = append_path_into_urlpatterns(urlpatterns, path)

    with open(urls_path, 'w') as file:
        file.write(imports + f'\n\napp_name = "{app_name}"\n' + urlpatterns)


def gen_url_imports(views: list[object], views_file_name: str):
    string_views = ", ".join((view.__name__ for view in views))

    return f"from django.urls import path\n\nfrom .{views_file_name} import {string_views}"


def gen_urlpatterns(views_module, app_name: str):
    views = import_views(views_module)
    urlpatterns = []

    for view in views:
        urlpatterns.append(gen_string_path(view, app_name))

    paths_string = ",\n    ".join(urlpatterns)

    result = f"""
urlpatterns = [
    {paths_string.strip()}
]    
    """

    return result


def gen_string_path(view, app_name) -> str:
    if has_path_decorator(view):
        path_name = get_decorator_path_name(view)
        path_url = get_decorator_path_url(view)

    else:
        path_name = get_path_name(view, app_name)
        path_url = get_path_url(path_name, detail=view_is_detail(view) if isclass(view) else False)

    if isclass(view):
        view_function = f"{view.__name__}.as_view()"
    else:
        view_function = f"{view.__name__}"

    return f'path("{path_url}", {view_function}, name="{path_name}")'


def separate_imports_and_urlpatterns(code: str) -> Tuple[str, str]:
    imports = ""
    urlpatterns = ""

    lines = code.splitlines()

    for i in range(len(lines)):
        if lines[i].startswith("from"):
            imports += lines[i] + "\n"

            if lines[i].endswith("("):
                x = i + 1
                while not lines[x].endswith(")"):
                    imports += lines[x] + "\n"
                    x += 1
                imports += lines[x] + "\n"

        if lines[i].startswith("urlpatterns"):
            for x in range(i, len(lines)):
                urlpatterns += lines[x] + "\n"
            break

    return imports, urlpatterns


def append_view_into_imports(imports: str, view: str):
    lines = imports.splitlines()

    for i in range(len(lines)):
        if lines[i].startswith("from .views"):
            if lines[i].endswith("("):
                x = i + 1
                while not lines[x].endswith(")"):
                    x += 1

                if lines[x].strip() == ")":
                    lines[x - 1] += ","
                    lines[x] = lines[x].replace(")", f"    {view}\n)")
                else:
                    lines[x] = lines[x].replace(")", f", {view})")

                break

            tokens = lines[i].split(" ")
            if view not in tokens:
                lines[i] += ", " + view

            break

    return "\n".join(lines)


def append_path_into_urlpatterns(urlpatterns: str, path: str):
    lines = urlpatterns.splitlines()
    lines = [line.rstrip() for line in lines]
    bracket = None

    for i, line in enumerate(lines):
        if "]" in line:
            bracket = i
            break

    if bracket:
        if not lines[bracket - 1].endswith(","):
            lines[bracket - 1] = lines[bracket - 1] + ","

        lines[bracket] = "    " + path
        lines.append("]")

    return "\n".join(lines)


def get_app_name(code: str) -> Optional[str]:
    lines = code.splitlines()

    for line in lines:
        if line.startswith("app_name"):
            pattern = r'"([^"]*)"'
            match = re.search(pattern, line)
            return match.group(1)

    return None
