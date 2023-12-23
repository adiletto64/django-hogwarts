import re
from dataclasses import dataclass
from typing import Optional

from hogwarts.utils import code_strip

FIELD_MAPPING = {
    'CharField': 'factory.Faker("name")',
    'TextField': 'factory.Faker("paragraph")',
    'EmailField': 'factory.Faker("email")',
    'URLField': 'factory.Faker("uri")',
    'IntegerField': 'factory.fuzzy.FuzzyInteger(0, 100)',
    'DateField': 'factory.Faker("date")',
    'DateTimeField': 'factory.Faker("date_time")',
    'BooleanField': 'factory.fuzzy.FuzzyChoice([True, False])',
}


def generate_factories_code(code: str):
    classes = split_model_classes(code)
    result = ""

    for cls in classes:
        result += "\n\n" + generate_factory_class(cls)

    imports = generate_imports(result)

    return imports + result


def generate_factory_class(model: str):
    model = flatten_multiline(model)
    lines = code_strip(model).splitlines()
    model_name = extract_class_name(lines[0])

    factory = f"class {model_name}Factory(factory.django.DjangoModelFactory):\n"

    for line in lines[1:]:
        new_line = change_field_to_faker(line)
        if new_line:
            factory += f"    {new_line}\n"

    factory += f"""
    class Meta:
        model = {model_name}
"""
    return factory


def change_field_to_faker(line: str):
    field = extract_field_meta(line.strip())
    if field:
        if "null=True" in field.args or "default=" in field.args:
            return None

        in_field_mapping = field.type.split(".")[-1] in FIELD_MAPPING.keys()
        if in_field_mapping:
            value = FIELD_MAPPING[field.type.split(".")[-1]]
            return f"{field.name} = {value}"


@dataclass
class Field:
    name: str
    type: str
    args: str


def extract_field_meta(field: str) -> Optional[Field]:
    match = re.match(r"(\w+) = (.*)\((.*)\)", field)
    if match:
        return Field(*match.groups())
    else:
        return None


def extract_class_name(line: str) -> Optional[str]:
    match = re.match(r"class\s+(.+?)\(", line)
    if match:
        return match.group(1)


def flatten_multiline(code: str) -> str:
    lines = code.splitlines()

    i = 0
    while i < len(lines):
        line = lines[i]
        if "(" in line and ")" not in line:
            lines[i] += lines[i + 1].strip()
            del lines[i + 1]

        else:
            i += 1

    return "\n".join(lines)


def generate_imports(factory_code):
    models = ", ".join(extract_meta_model(factory_code))
    has_fuzzy = "fuzzy" in factory_code

    imports = "import factory"
    if has_fuzzy:
        imports += "\nfrom factory import fuzzy"

    imports += f"\n\nfrom .models import {models}\n"

    return imports


def extract_meta_model(code: str) -> list[str]:
    lines = code.splitlines()
    models = []

    for i in range(len(lines)):
        if "model = " in lines[i]:
            models.append(lines[i].split("=")[-1].strip())

    return models


def split_model_classes(code: str) -> list[str]:
    class_blocks = ["class " + block.strip() + "\n" for block in code_strip(code).split("class ")[1:] if "models.Model" in block]
    return class_blocks
