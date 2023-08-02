from django.core.management.base import BaseCommand

from hogwarts.magic_urls.genurls import gen_urls_py
from .base import get_app_config, get_views_module


class Command(BaseCommand):
    help = "urlpatterns generation from views.py"

    def add_arguments(self, parser):
        parser.add_argument("app", type=str)

    def handle(self, *args, **options):
        app_name: str = options["app"]

        views_module = get_views_module(app_name)
        app_config = get_app_config(app_name)
        urls_path = f'{app_config.path}\\urls.py'

        gen_urls_py(views_module, urls_path)

        self.stdout.write(
            self.style.SUCCESS("Successfully generated urls 🔥")
        )
