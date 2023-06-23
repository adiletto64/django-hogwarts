from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

from hogwarts.codegen import generate_views


class Command(BaseCommand):
    help = "Code generation command"

    def add_arguments(self, parser):
        parser.add_argument("app", type=str)
        parser.add_argument("model", type=str)

    def handle(self, *args, **options):
        app_name: str = options["app"]
        model_name: str = options["model"]

        app_names = [_app.name for _app in apps.get_app_configs()]

        if app_name not in app_names:
            raise CommandError(f"Provided app '{app_name}' does not exist")

        app_config = apps.get_app_config(app_name)

        if model_name.lower() not in app_config.models.keys():
            raise CommandError(f"Provided model '{model_name}' does not exist in app '{app_name}'")

        model = app_config.models.get(model_name.lower())
        code = generate_views(model)

        path = f'{app_config.path}\\generated_views.py'
        with open(path, 'w') as file:
            file.write(code)

        self.stdout.write(
            self.style.SUCCESS(f"Generated CRUD views in {path}")
        )


