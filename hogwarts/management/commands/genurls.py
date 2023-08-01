import importlib

from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

from hogwarts.magic_urls.genurls import gen_urls


class Command(BaseCommand):
    help = "urlpatterns generation from views.py"

    def add_arguments(self, parser):
        parser.add_argument("app", type=str)

    def handle(self, *args, **options):
        app_name: str = options["app"]

        try:
            apps.get_app_config(app_name)
        except LookupError:
            raise CommandError(f"App '{app_name}' does not exist.")

        try:
            # Import the views.py file dynamically
            views_module = importlib.import_module(f"{app_name}.views")
        except ModuleNotFoundError:
            raise CommandError(f"Views not found for app '{app_name}'.")

        print(gen_urls(views_module, "example"))

        self.stdout.write(
            self.style.SUCCESS("Successfully generated urls 🔥")
        )
