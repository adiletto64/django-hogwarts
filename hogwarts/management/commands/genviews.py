import os

from django.core.management.base import BaseCommand, CommandError

from .base import get_app_config
from hogwarts.magic_views import ViewGenerator
from ...utils import parse_class_names


class Command(BaseCommand):
    help = "Code generation command"

    def add_arguments(self, parser):
        parser.add_argument("app", type=str)
        parser.add_argument("model", type=str)
        parser.add_argument(
            "--smart-mode", "-s",
            action="store_true",
            help="sets login required to create and update actions"
        )

        parser.add_argument(
            "--model-is-namespace", "-mn",
            action="store_true",
            help="sets app name as namespace and action as endpoint for edit views."
                 "see https://docs.djangoproject.com/en/4.2/topics/http/urls/#reversing-namespaced-urls"
                 "or try for yourself"
        )

    def handle(self, *args, **options):
        app_name: str = options["app"]
        model_name: str = options["model"]
        smart_mode: bool = options["smart_mode"]
        model_is_namespace: bool = options["model_is_namespace"]

        app_config = get_app_config(app_name)

        model = app_config.models.get(model_name.lower())
        if model is None:
            raise CommandError(f"Provided model '{model_name}' does not exist in app '{app_name}'")

        namespace_model = False
        if model_is_namespace or model_name.lower() in app_name:
            namespace_model = True

        path = os.path.join(app_config.path, "views.py")

        generator = ViewGenerator(model, smart_mode, namespace_model)

        with open(path, "r") as file:
            existing_code = file.read()
            is_empty = len(parse_class_names(existing_code)) == 0
            if not is_empty:
                generator = ViewGenerator(model, smart_mode, namespace_model, code=existing_code)

        code = generator.gen()

        with open(path, 'w') as file:
            file.write(code)

        self.stdout.write(
            self.style.SUCCESS(f"Generated CRUD views in {path}")
        )
