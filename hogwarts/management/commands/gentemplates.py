from django.core.management.base import BaseCommand, CommandError

from .base import get_app_config


class Command(BaseCommand):
    help = "Code generation command"

    def add_arguments(self, parser):
        parser.add_argument("app", type=str)
        parser.add_argument("model", type=str)

    def handle(self, *args, **options):
        app_name: str = options["app"]
        model_name: str = options["model"]

        app_config = get_app_config(app_name)

        model = app_config.models.get(model_name.lower())
        if model is None:
            raise CommandError(f"Provided model '{model_name}' does not exist in app '{app_name}'")

        urls_py = open(f"{app_config.path}\\urls.py")

        path = f'{app_config.path}\\views.py'
        with open(path, 'w') as file:
            pass

        self.stdout.write(
            self.style.SUCCESS(f"Generated CRUD views in {path}")
        )
