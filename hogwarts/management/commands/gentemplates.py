from django.core.management.base import BaseCommand, CommandError

from .base import get_app_config


class Command(BaseCommand):
    help = "Code generation command"

    def add_arguments(self, parser):
        parser.add_argument("app", type=str)

    def handle(self, *args, **options):
        app_name: str = options["app"]
        app_config = get_app_config(app_name)


