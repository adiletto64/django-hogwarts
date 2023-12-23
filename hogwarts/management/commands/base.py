import importlib
import os

from django.core.management.base import CommandError
from django.apps import apps


def get_app_config(app_name: str):
    try:
        return apps.get_app_config(app_name)
    except LookupError:
        raise CommandError(f"App '{app_name}' does not exist.")


def get_views_module(app_name: str):
    module = apps.get_app_config(app_name).name
    try:
        # Import the views.py file dynamically
        return importlib.import_module(f"{module}.views")
    except ModuleNotFoundError:
        raise CommandError(f"Views not found for app '{app_name}'.")


def get_models_py_code(app_name: str):
    # reads and returns models.py code from app_name
    module = apps.get_app_config(app_name)
    path = os.path.join(module.path, "models.py")

    with open(path, "r") as file:
        return file.read()
