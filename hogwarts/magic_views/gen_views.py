from typing import Type, Optional, Tuple

from django.db import models

from ..utils import to_plural, code_strip, remove_empty_lines


def generate_views(model: Type[models.Model]):
    gen = ViewGenerator(model)

    detail = gen.gen_detail_view()
    _list = gen.gen_list_view()
    create = gen.gen_create_view()
    update = gen.gen_update_view()

    return merge_views_and_imports([detail, _list, create, update], gen.get_imports_code())


def merge_views_and_imports(view_code_blocks: list[str], imports: str):
    origin_code = code_strip(imports)

    for code in view_code_blocks:
        origin_code += f"\n{code_strip(code)}"

    return origin_code


class ViewGenerator:
    def __init__(self, model: Type[models.Model]):
        self.model = model
        self.model_name = model.__name__
        self.model_name_lower = self.model_name.lower()

        self.generic_views = []
        self.extra_imports = []

    def get_imports_code(self):
        imports_generator = ImportsGenerator()
        imports_generator.add_bulk("django.views.generic", self.generic_views)
        imports_generator.add(".models", self.model_name)

        return imports_generator.gen()

    def gen_detail_view(self):
        self.generic_views.append("DetailView")
        return self.base_view("detail", False, True, True)

    def gen_list_view(self):
        self.generic_views.append("ListView")
        return self.base_view("list", False, True)

    def gen_create_view(self):
        self.generic_views.append("CreateView")
        return self.base_view("create", True, False)

    def gen_update_view(self):
        self.generic_views.append("UpdateView")
        return self.base_view("update", True, False)

    def base_view(
            self,
            action: str,
            set_fields: bool,
            context: bool,
            detail: bool = False,
            mixins: list[str] = [],
            extra_code: Optional[str] = None
    ):
        name = self.model_name_lower

        class_name = f"{self.model_name}{action.capitalize()}View"
        object_name = name if detail else to_plural(name)
        template_name = f"{to_plural(name)}/{name}_{action.lower()}.html"
        inherits = ""
        if mixins:
            inherits += ", ".join(mixins) + ", "
        inherits += f"{action.capitalize()}View"

        fields = self.model._meta.fields
        field_names = [field.name for field in fields]

        result = f"""
        class {class_name}({inherits}):
            model = {self.model_name}
            {f'fields = {str(field_names)}' if set_fields else ''}
            {f'context_object_name = "{object_name}"' if context else ''}
            template_name = "{template_name}"
        """

        result = remove_empty_lines(result)

        if extra_code:
            extra_code = "\n".join(map(lambda line: " " * 8 + line, extra_code.splitlines()))
            extra_code = remove_empty_lines(extra_code)
            result += f"\n\n{extra_code}"

        return result + "\n"

    @property
    def imports(self):
        return [self.model_name] + self.generic_views


Imports = list[Tuple[str, str]]


class ImportsGenerator:
    def __init__(self):
        self.imports: Imports = []

    def add(self, module, obj):
        self.imports.append((module, obj))

    def add_bulk(self, module, objs: list[str]):
        for obj in objs:
            self.add(module, obj)

    def gen(self):
        merged_imports = {}

        for module, obj in self.imports:
            if module not in merged_imports.keys():
                merged_imports[module] = [obj]
            else:
                merged_imports[module].append(obj)

        result = ""
        for module, obj in merged_imports.items():
            result += f"from {module} import {', '.join(obj)}\n"

        return result
