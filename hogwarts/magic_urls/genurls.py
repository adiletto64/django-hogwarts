from inspect import isclass

from hogwarts.magic_urls.base import (
    import_views,
    get_path_name,
    get_path_url,
    Path,
    view_is_detail,
    has_path_decorator,
    get_decorator_path_name,
    get_decorator_path_url
)


def gen_urls(views_module, app_name: str):
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
