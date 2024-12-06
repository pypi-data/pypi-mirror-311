__version__ = "0.0.6"

import os

import yaml
from jinja2 import BaseLoader, Environment

from quicks.exceptions import PathExistsError

__all__ = (
    "__version__",
    "get_env",
    "parse_template",
    "parse_template_by_stream",
    "process_project",
)


TEMPLATE_VERSIONS = (1,)


def get_env():
    """Returned jinja2 Environment"""
    return Environment(loader=BaseLoader)


def process_project(env, path, project, template, interactive=False, encoding="utf-8"):
    """Process project generate"""
    project_path = os.path.join(path, project)
    _raise_for_exists_path(project_path)

    project_files, templates, configs, *_ = template
    kwargs = dict(project=project, configs={})

    for config_name, value in configs.items():
        if isinstance(value, str):
            config_type = str
            default_value = env.from_string(value).render(**kwargs)
        elif isinstance(value, (int, float)):
            config_type = type(value)
            default_value = value
        else:
            raise ValueError

        if interactive:
            val = input(f"{config_name} ({default_value}):")
            if config_type is bool:
                kwargs["configs"][config_name] = val.lower() in ("1", "true")
            elif val:
                kwargs["configs"][config_name] = config_type(val)
            else:
                kwargs["configs"][config_name] = default_value
        else:
            kwargs["configs"][config_name] = default_value

    os.makedirs(project_path)

    for file in project_files:
        alias = None
        if isinstance(file, list):
            file, alias, *_ = file
        file_template = env.from_string(templates.get(alias or file, "")).render(
            **kwargs
        )
        file_name = env.from_string(file).render(**kwargs)
        if not file_name:
            continue
        file_path = os.path.join(project_path, file_name)
        file_dir = os.path.dirname(file_path)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        with open(file_path, "w", encoding=encoding) as f:
            f.write(file_template)


def parse_template(path, encoding="utf-8"):
    """Parse yaml project template by file path"""
    with open(path, encoding=encoding) as f:
        return parse_template_by_stream(f)


def parse_template_by_stream(stream):
    """Parse yaml project template"""
    data = yaml.load(stream, yaml.FullLoader)

    return (
        data.get("files", []),
        data.get("templates", {}),
        data.get("configs", {}),
        data.get("version", 0),
    )


def _raise_for_exists_path(project_path):
    """Checking exists path"""
    if os.path.exists(project_path):
        raise PathExistsError
