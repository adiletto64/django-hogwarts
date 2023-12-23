import os

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from rich.console import Console

from hogwarts.magic_tests.template import gen_tests
from .base import get_app_config


console = Console()

class Command(BaseCommand):
    help = "Code generation command"

    def add_arguments(self, parser):
        parser.add_argument("app", type=str)

    def handle(self, *args, **options):
        app_name: str = options["app"]

        try:
            call_command("genfactories", app_name)
        except CommandError as e:
            self.stderr.write(self.style.ERROR(f"Could not generate factories for models in {app_name}: {e}"))

        console.print(f"generating tests for endpoints in '{app_name}.urls'...", style="bright_black")

        try:
            result = gen_tests(app_name)

            app_config = get_app_config(app_name)
            tests_path = os.path.join(app_config.path, "tests.py")
            with open(tests_path, "w") as file:
                file.write(result)

            console.print("result tests.py:", style="green")
            console.print("===========================================")
            console.print(result, style="bright_black on gray11")
            console.print("===========================================")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Could not generate tests for views in {app_name}: {e}"))
