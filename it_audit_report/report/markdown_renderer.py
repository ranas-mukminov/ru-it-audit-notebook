from pathlib import Path
from typing import Dict

from jinja2 import Environment, FileSystemLoader, select_autoescape


def render_markdown(template_path: Path, context: Dict) -> str:
    env = Environment(
        loader=FileSystemLoader(template_path.parent),
        autoescape=select_autoescape(enabled_extensions=("html", "xml")),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template(template_path.name)
    return template.render(**context)
