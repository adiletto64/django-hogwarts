import importlib
from dataclasses import dataclass
from typing import Optional, TypeVar, Type
import inspect

from django.conf import settings
from django.core.exceptions import ViewDoesNotExist
from django.urls import URLPattern, URLResolver
from django.apps import apps
from django.views.generic import CreateView, UpdateView, View

from hogwarts.magic_urls.base import camel_to_snake
from hogwarts.utils import is_camel_case


@dataclass
class Endpoint:
    view: object
    path: str
    url_name: str
    factory: Optional[object] = None

    def get_view_name(self):
        if hasattr(self.view, 'view_class'):
            return self.view.view_class.__name__
        return self.view.__name__


    def find_factory(self, app_name):
        model = self.get_view_model()
        if not model:
            return

        module_name = apps.get_app_config(app_name).name
        try:
            factory_code = importlib.import_module(f"{module_name}.factories")
        except ModuleNotFoundError:
            return

        all_classes = inspect.getmembers(factory_code, inspect.isclass)

        for name, cls in all_classes:
            if hasattr(cls, '_meta') and hasattr(cls._meta, 'factory') and cls._meta.model == model:
                self.factory = cls
                return


    def get_view_model(self):
        if hasattr(self.view, 'view_class') and hasattr(self.view.view_class, 'model'):
            return self.view.view_class.model
        else:
            return None


ViewClass = TypeVar('ViewClass', bound=View)

def get_fields(view_class: Type[ViewClass]) -> Optional[list[object]]:
    """
    get fields from view's "fields" attr or from form_class
    """
    fields: Optional[list] = None
    model = view_class.model

    if not model:
        if hasattr(view_class, 'form_class'):
            model = view_class.form_class.model
        else:
            return None

    if issubclass(view_class, CreateView) or issubclass(view_class, UpdateView):
        if view_class.fields:
            fields = view_class.fields
        elif hasattr(view_class, 'form_class'):
            fields = list(view_class.form_class.fields)

    if not fields:
        return None

    return [field for field in model._meta.fields if field.name in fields]



def create_test_name(view_name: str):
    if is_camel_case(view_name):
        view_name = camel_to_snake(view_name)

    if view_name.endswith("view"):
        view_name = view_name[:-4]

    view_name = view_name.strip("_")

    return f"test_{view_name}"


def import_app_endpoints(app_name) -> list[Endpoint]:
    urlconf = __import__(getattr(settings, 'ROOT_URLCONF'), {}, {}, [''])

    endpoints = extract_views_from_urlpatterns(urlconf.urlpatterns)
    endpoints = filter(lambda e: e.view.__module__.startswith(app_name), endpoints)

    return list(endpoints)


# original code from:
# https://github.com/django-extensions/django-extensions/blob/main/django_extensions/management/commands/show_urls.py
def extract_views_from_urlpatterns(urlpatterns, base='', namespace=None):
    """
    Return a list of views from a list of urlpatterns.
    Each object in the returned list is a three-tuple: (view_func, regex, name)
    """
    class RegexURLPattern: pass
    class RegexURLResolver: pass
    def describe_pattern(p): return str(p.pattern)

    views: list[Endpoint] = []

    for p in urlpatterns:
        if isinstance(p, (URLPattern, RegexURLPattern)):
            try:
                if not p.name:
                    name = p.name
                elif namespace:
                    name = '{0}:{1}'.format(namespace, p.name)
                else:
                    name = p.name
                pattern = describe_pattern(p)
                views.append(Endpoint(p.callback, base + pattern, name))
            except ViewDoesNotExist:
                continue
        elif isinstance(p, (URLResolver, RegexURLResolver)):
            try:
                patterns = p.url_patterns
            except ImportError:
                continue
            if namespace and p.namespace:
                _namespace = '{0}:{1}'.format(namespace, p.namespace)
            else:
                _namespace = (p.namespace or namespace)
            pattern = describe_pattern(p)
            views.extend(extract_views_from_urlpatterns(patterns, base + pattern, namespace=_namespace))
        elif hasattr(p, '_get_callback'):
            try:
                views.append(Endpoint(p._get_callback(), base + describe_pattern(p), p.name))
            except ViewDoesNotExist:
                continue
        elif hasattr(p, 'url_patterns') or hasattr(p, '_get_url_patterns'):
            try:
                patterns = p.url_patterns
            except ImportError:
                continue
            views.extend(extract_views_from_urlpatterns(patterns, base + describe_pattern(p), namespace=namespace))
        else:
            raise TypeError("%s does not appear to be a urlpattern object" % p)
    return views
