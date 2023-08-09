from typing import Type, Tuple

from django.db import models

from ..utils import to_plural, code_strip, remove_empty_lines


def generate_views(model: Type[models.Model], smart_mode=False, model_is_namespace=False):
    gen = ViewGenerator(model, smart_mode, model_is_namespace)

    detail = gen.detail()
    _list = gen.list()
    create = gen.create()
    update = gen.update()

    return merge_views_and_imports([detail, _list, create, update], gen.gen_imports())


def merge_views_and_imports(view_code_blocks: list[str], imports: str):
    origin_code = code_strip(imports)

    for code in view_code_blocks:
        origin_code += f"\n\n{code_strip(code)}"

    return origin_code


class ViewGenerator:
    def __init__(self, model, smart_mode=False, model_is_namespace=False):
        self.model_name = model.__name__
        self.name = model.__name__.lower()
        self.fields = [field.name for field in model._meta.fields]
        self.imports_generator = ImportsGenerator()
        self.generic_views = []
        self.smart_mode = smart_mode
        self.model_is_namespace = model_is_namespace

    def gen_imports(self):
        self.imports_generator.add_bulk("django.views.generic", self.generic_views)
        self.imports_generator.add(".models", self.model_name)

        return self.imports_generator.gen()

    def create(self):
        self.generic_views.append("CreateView")

        builder = self.get_builder("create")

        if self.smart_mode:
            self.imports_generator.add_login_required()
            builder = self.get_builder("create", ["LoginRequiredMixin"])

        builder.add_fields(self.fields)
        self.add_template(builder, "create")
        if not self.model_is_namespace:
            builder.add_success_url("/")

        if self.smart_mode:
            for field in self.fields:
                if field in ["user", "author", "owner", "creator"]:
                    function = f"""
                    def form_valid(self, form):
                        form.instance.{field} = self.request.user
                        return super().form_valid(form)
                    """
                    builder.add_extra_code(code_strip(function))
                    break

        if self.model_is_namespace:
            self.imports_generator.add_reverse()
            function = f"""
            def get_success_url(self):
                return reverse("{to_plural(self.name)}:detail", args=[self.object.id])
            """
            builder.add_extra_code(code_strip(function))

        return builder.result

    def update(self):
        self.generic_views.append("UpdateView")
        builder = self.get_builder("update")

        if self.smart_mode:
            self.imports_generator.add_user_test()
            builder = self.get_builder("update", ["UserPassesTestMixin"])

        builder.add_fields(self.fields)
        self.add_template(builder, "update")
        if not self.model_is_namespace:
            builder.add_success_url("/")

        if self.smart_mode:
            for field in self.fields:
                if field in ["user", "author", "owner", "creator"]:
                    function = """
                    def test_func(self):
                        return self.get_object() == self.request.user
                    """
                    builder.add_extra_code(code_strip(function))
                    break

        if self.model_is_namespace:
            self.imports_generator.add_reverse()
            function = f"""
            def get_success_url(self):
                return reverse("{to_plural(self.name)}:detail", args=[self.get_object().id])
            """
            builder.add_extra_code(code_strip(function))

        return builder.result

    def detail(self):
        self.generic_views.append("DetailView")
        builder = self.get_builder("detail")
        builder.add_context_object_name(self.name)
        self.add_template(builder, "detail")

        return builder.result

    def list(self):
        self.generic_views.append("ListView")
        builder = self.get_builder("list")
        builder.add_context_object_name(to_plural(self.name))
        self.add_template(builder, "list")

        return builder.result

    def get_builder(self, action, mixins=[]):
        builder = ClassViewBuilder(self.model_name)
        builder.add_class(action, mixins)
        builder.add_model()

        return builder

    def add_template(self, builder, action):
        builder.add_template_name(f"{to_plural(self.name)}/{self.name}_{action}.html")


class ClassViewBuilder:
    def __init__(self, model_name):
        self.model_name = model_name
        self.result = ""

    def add_class(self, action, mixins=[]):
        action = action.capitalize()
        class_name = f"{self.model_name}{action}View"
        inherits = [*mixins, f"{action}View"]

        self.result += f"class {class_name}({', '.join(inherits)}):\n"

    def add_model(self):
        self.result += f'    model = {self.model_name}\n'

    def add_fields(self, fields: list[str]):
        fields = [f'"{field}"' for field in fields]
        self.result += f"    fields = [{', '.join(fields)}]\n"

    def add_context_object_name(self, name):
        self.result += f'    context_object_name = "{name}"\n'

    def add_template_name(self, name):
        self.result += f'    template_name = "{name}"\n'

    def add_success_url(self, url):
        self.result += f'    success_url = "{url}"\n'

    def add_extra_code(self, extra_code):
        extra_code = "\n".join(map(lambda line: " " * 4 + line, extra_code.splitlines()))
        extra_code = remove_empty_lines(extra_code)

        self.result += f"\n{extra_code}\n"


Imports = list[Tuple[str, str]]


class ImportsGenerator:
    def __init__(self):
        self.imports: Imports = []

    def add(self, module, obj):
        self.imports.append((module, obj))

    def add_bulk(self, module, objs: list[str]):
        for obj in objs:
            self.add(module, obj)

    def add_login_required(self):
        obj = "LoginRequiredMixin"
        if not self.exists(obj):
            self.add("django.contrib.auth.mixins", obj)

    def add_user_test(self):
        obj = "UserPassesTestMixin"
        if not self.exists(obj):
            self.add("django.contrib.auth.mixins", obj)

    def add_reverse(self):
        obj = "reverse"
        if not self.exists(obj):
            self.add("django.shortcuts", obj)

    def add_reverse_lazy(self):
        obj = "reverse_lazy"
        if not self.exists(obj):
            self.add("django.shortcuts", obj)

    def exists(self, obj: str):
        return any(i[1] == obj for i in self.imports)

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

    @property
    def imported_classes(self):
        for _import in self.imports:
            yield _import[1]
