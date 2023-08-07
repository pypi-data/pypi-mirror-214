import re


def to_snake_case(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("__([A-Z])", r"_\1", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()


def prettify_name(name: str) -> str:
    """Prettify a string replacing underscores with spaces"""
    return re.sub(r"_+", " ", name).strip()


def get_job_id(pipeline_id: str, trigger_id: str) -> str:
    return f"{pipeline_id}: {trigger_id}"
