from hogwarts.utils import code_strip

from .testcase import create_test_name, get_fields

from .constants import TEST_FIELDS


def create_detail_test(view_class, factory, url_name):
    test_name = create_test_name(view_class.__name__)
    model_name = view_class.model.__name__.lower()

    result = f"""
    def {test_name}(self):
        {model_name} = {factory.__name__}()

        response = self.client.get(reverse("{url_name}", args=[{model_name}.pk]))

        self.assertEqual(response.status_code, 200)
    """

    return code_strip(result)


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

    return code_strip(result)


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

    return code_strip(result)


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

    return code_strip(result)


def get_payload_string(fields):
    fields_string = "payload = {"

    for field in fields:
        fields_string += f'\n            "{field.name}": {TEST_FIELDS[field.__class__]},'

    fields_string += "\n        }\n"
    return fields_string
