import os

from django.core.management.base import BaseCommand
from rich.console import Console

from .base import get_app_config, get_models_py_code
from hogwarts.magic_tests.factory import generate_factories_code

console = Console()


class Command(BaseCommand):
    help = "factory classes generation (factory_boy) from models.py"

    def add_arguments(self, parser):
        parser.add_argument("app_name", type=str)

    def handle(self, *args, **options):
        app_name: str = options["app_name"]

        app_config = get_app_config(app_name)
        console.print(f"generating factories for models.py in '{app_name}'...", style="bright_black")
        factories_path = os.path.join(app_config.path, "factories.py")
        models_code = get_models_py_code(app_name)
        factories_code = generate_factories_code(models_code)

        console.print("result factories.py:", style="green")
        console.print("===========================================")
        console.print(factories_code, style="bright_black on gray11")
        console.print("===========================================")

        with open(factories_path, "w") as file:
            file.write(factories_code)
