import math
from typing import Type
from dataclasses import dataclass

from django.db import models

from .utils import to_plural


@dataclass
class ClassView:
    imports: set[str]
    name: str
    code: str


class ViewGenerator:
    def __init__(self, model: Type[models.Model]):
        self.model = model
        self.model_name = model.__name__
        self.model_name_lower = self.model_name.lower()

        self.fields = model._meta.fields
        self.field_names = [field.name for field in self.fields]

    def gen_detail_view(self):
        return f"""
            class {self.model_name}DetailView(DetailView):
                model = {self.model_name}
                context_object_name = "{self.model_name_lower}"
                template_name = "{to_plural(self.model_name_lower)}/{self.model_name_lower}_detail.html"
        """

    def gen_list_view(self):
        return f"""
            class {self.model_name}CreateView(CreateView):
                model = {self.model_name}
                context_object_name = "{to_plural(self.model_name_lower)}"
                template_name = "{to_plural(self.model_name_lower)}/{self.model_name_lower}_create.html"
        """

    def gen_create_view(self):
        return f"""
            class {self.model_name}CreateView(CreateView):
                model = {self.model_name}
                fields = {str(self.field_names)}
                template_name = "{to_plural(self.model_name_lower)}/{self.model_name_lower}_create.html"
        """

    def gen_update_view(self):
        return f"""
            class {self.model_name}UpdateView(UpdateView):
                model = {self.model_name}
                fields = {str(self.field_names)}
                template_name = "{to_plural(self.model_name_lower)}/{self.model_name_lower}_update.html"
        """
