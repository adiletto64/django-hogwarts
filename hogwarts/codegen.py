import math
from typing import Type
from dataclasses import dataclass

from django.db import models

from .utils import to_plural, code_strip

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
        self.imports = [self.model_name]
        self.class_names = []

    def get_imports_code(self):
        imports = self.imports[1:]
        return f"""
        from django.views.generic import {", ".join(imports)}
        from .models import {self.model_name}
        """

    def gen_detail_view(self):
        self.imports.append("DetailView")
        self.add_class(f"{self.model_name}DetailView")

        return f"""
            class {self.model_name}DetailView(DetailView):
                model = {self.model_name}
                context_object_name = "{self.model_name_lower}"
                template_name = "{to_plural(self.model_name_lower)}/{self.model_name_lower}_detail.html"
        """

    def gen_list_view(self):
        self.imports.append("ListView")
        self.add_class(f"{self.model_name}ListView")

        return f"""
            class {self.model_name}ListView(ListView):
                model = {self.model_name}
                context_object_name = "{to_plural(self.model_name_lower)}"
                template_name = "{to_plural(self.model_name_lower)}/{self.model_name_lower}_list.html"
        """

    def gen_create_view(self):
        self.imports.append("CreateView")
        self.add_class(f"{self.model_name}CreateView")

        return f"""
            class {self.model_name}CreateView(CreateView):
                model = {self.model_name}
                fields = {str(self.field_names)}
                template_name = "{to_plural(self.model_name_lower)}/{self.model_name_lower}_create.html"
        """

    def gen_update_view(self):
        self.imports.append("UpdateView")
        self.add_class(f"{self.model_name}UpdateView")

        return f"""
            class {self.model_name}UpdateView(UpdateView):
                model = {self.model_name}
                fields = {str(self.field_names)}
                template_name = "{to_plural(self.model_name_lower)}/{self.model_name_lower}_update.html"
        """

    def add_class(self, class_name: str):
        if class_name not in self.class_names:
            self.class_names.append(class_name)


def insert_code(code_blocks: list[str], imports: str):
    origin_code = code_strip(imports)

    for code in code_blocks:
        origin_code += f"\n{code_strip(code)}"

    return origin_code
