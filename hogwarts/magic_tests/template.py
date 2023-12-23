from django.views.generic import CreateView, UpdateView, ListView, DetailView

from hogwarts.utils import code_strip

from .testcase import create_test_name, get_fields, import_app_endpoints
from .constants import TEST_FIELDS


def gen_tests(app_name):
    endpoints = import_app_endpoints(app_name)
    result = gen_imports(app_name)

    result += f"""
    
class {endpoints[0].get_view_model().__name__}TestCase(TestCase):"""

    for endpoint in endpoints:
        if hasattr(endpoint.view, 'view_class'):
            view_class = endpoint.view.view_class
            endpoint.find_factory(app_name)

            if issubclass(view_class, CreateView):
                result += create_create_test(view_class, endpoint.url_name)
            elif issubclass(view_class, UpdateView):
                result += create_update_test(view_class, endpoint.factory, endpoint.url_name)
            elif issubclass(view_class, ListView):
                result += create_list_test(view_class, endpoint.factory, endpoint.url_name)
            elif issubclass(view_class, DetailView):
                result += create_detail_test(view_class, endpoint.factory, endpoint.url_name)


    print(result)
    return code_strip(result)


def gen_imports(app_name):
    endpoints = import_app_endpoints(app_name)

    result = """
        from django.tests import TestCase
        from django.shortcuts import reverse
    """

    models = []

    for endpoint in endpoints:
        model = endpoint.get_view_model()
        if model and model not in models:
            models.append(model)

    result += f"""
        from {app_name}.models import {', '.join([model.__name__ for model in models])}\n"""

    factories = []
    for endpoint in endpoints:
        endpoint.find_factory(app_name)
        if endpoint.factory:
            factories.append(endpoint.factory.__name__)

    factories = list(set(factories))

    result += f"""        from {app_name}.factories import {', '.join(factories)}
    """

    return code_strip(result)


def create_detail_test(view_class, factory, url_name):
    test_name = create_test_name(view_class.__name__)
    model_name = view_class.model.__name__

    object_create = f"{factory.__name__}()" if factory else f"{model_name}.objects.create()  # TODO: add fields manually"

    result = f"""
    def {test_name}(self):
        {model_name.lower()} = {object_create}

        response = self.client.get(reverse("{url_name}", args=[{model_name.lower()}.pk]))

        self.assertEqual(response.status_code, 200)
    """

    return result


def create_list_test(view_class, factory, url_name):
    test_name = create_test_name(view_class.__name__)
    context_object_name = view_class().get_context_object_name(view_class.model.objects.all())

    result = f"""
    def {test_name}(self):
        {factory.__name__}.create_batch(3)

        response = self.client.get(reverse("{url_name}"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["{context_object_name}"]), 3)
    """

    return result


def create_create_test(view_class, url_name):
    test_name = create_test_name(view_class.__name__)
    model_name = view_class.model.__name__

    fields = get_fields(view_class)
    fields_string = ""

    if fields:
        fields_string = get_payload_string(fields)

    result = f"""
    def {test_name}(self):
        {fields_string}
        response = self.client.post(reverse("{url_name}"), payload)

        self.assertEqual(response.status_code, 302)
        self.assertTrue({model_name}.objects.exists())
    """

    return result


def create_update_test(view_class, factory, url_name):
    test_name = create_test_name(view_class.__name__)
    model_name = view_class.model.__name__.lower()

    fields = get_fields(view_class)
    fields_string = get_payload_string(fields)

    result = f"""
    def {test_name}(self):
        {model_name} = {factory.__name__}()

        {fields_string}
        response = self.client.post(reverse("{url_name}", args=[{model_name}.pk]), payload)
        {model_name}.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual({model_name}.{fields[0].name}, payload["{fields[0].name}"])
    """

    return result


def get_payload_string(fields):
    fields_string = "payload = {"

    for field in fields:
        fields_string += f'\n            "{field.name}": {TEST_FIELDS[field.__class__]},'

    fields_string += "\n        }\n"
    return fields_string
