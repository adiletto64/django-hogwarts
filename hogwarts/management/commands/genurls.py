import importlib

from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

from hogwarts.magic_urls._base import import_views
from hogwarts.magic_urls.genurls import gen_urls, gen_url_imports


class Command(BaseCommand):
    help = "urlpatterns generation from views.py"

    def add_arguments(self, parser):
        parser.add_argument("app", type=str)

    def handle(self, *args, **options):
        app_name: str = options["app"]

        try:
            app_config = apps.get_app_config(app_name)
        except LookupError:
            raise CommandError(f"App '{app_name}' does not exist.")

        try:
            # Import the views.py file dynamically
            views_module = importlib.import_module(f"{app_name}.views")
        except ModuleNotFoundError:
            raise CommandError(f"Views not found for app '{app_name}'.")

        imports = gen_url_imports(import_views(views_module), "views")
        urlpatterns = gen_urls(views_module, "example")

        print(f"generating urls for {app_name}.views 📂")

        print("======resulting urlpatterns========")
        print(urlpatterns)

        path = f'{app_config.path}\\urls.py'
        with open(path, 'w') as file:
            file.write(imports + "\n\n" + urlpatterns)

        self.stdout.write(
            self.style.SUCCESS("Successfully generated urls 🔥")
        )
