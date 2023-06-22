def to_plural(string: str):
    return string if string.endswith("s") else f"{string}s"
