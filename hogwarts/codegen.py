import math
from typing import Type
from dataclasses import dataclass

from django.db import models

from .utils import to_plural, code_strip, remove_empty_lines

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
        return self.base_view("detail", False, True, True)

    def gen_list_view(self):
        self.imports.append("ListView")
        self.add_class(f"{self.model_name}ListView")
        return self.base_view("list", False, True)


    def gen_create_view(self):
        self.imports.append("CreateView")
        self.add_class(f"{self.model_name}CreateView")
        return self.base_view("create", True, False)

    def gen_update_view(self):
        self.imports.append("UpdateView")
        self.add_class(f"{self.model_name}UpdateView")
        return self.base_view("update", True, False)

    def base_view(self, action: str, fields: bool, context: bool, detail: bool = False):
        name = self.model_name_lower
        action_view = f"{action.capitalize()}View"
        object_name = name if detail else to_plural(name)
        template_name = f"{to_plural(name)}/{name}_{action.lower()}.html"

        result = f"""
        class {self.model_name}{action_view}({action_view}):
            model = {self.model_name}
            {f'fields = {str(self.field_names)}' if fields else ''}
            {f'context_object_name = "{object_name}"' if context else ''}
            template_name = "{template_name}"
        """

        return remove_empty_lines(result) + "\n"

    def add_class(self, class_name: str):
        if class_name not in self.class_names:
            self.class_names.append(class_name)


def insert_code(code_blocks: list[str], imports: str):
    origin_code = code_strip(imports)

    for code in code_blocks:
        origin_code += f"\n{code_strip(code)}"

    return origin_code


def generate_views(model: Type[models.Model]):
    gen = ViewGenerator(model)

    detail = gen.gen_detail_view()
    _list = gen.gen_list_view()
    create = gen.gen_create_view()
    update = gen.gen_update_view()

    return insert_code([detail, _list, create, update], gen.get_imports_code())
