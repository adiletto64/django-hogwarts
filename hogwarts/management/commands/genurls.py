from django.core.management.base import BaseCommand, CommandError
from django.apps import apps


class Command(BaseCommand):
    help = "urlpatterns generation from views.py"

    def add_arguments(self, parser):
        parser.add_argument("app", type=str)

    def handle(self, *args, **options):
        app_name: str = options["app"]

        app_names = [_app.name for _app in apps.get_app_configs()]

        if app_name not in app_names:
            raise CommandError(f"Provided app '{app_name}' does not exist")

        apps.get_app_config(app_name)

        self.stdout.write(
            self.style.SUCCESS("Successfully generated urls 🔥")
        )
