from pathlib import Path

import jinja2

from . import TemplateData
from .renderer import Renderer


class JinjaRenderer(Renderer):
    def __init__(self, environment: jinja2.Environment) -> None:
        self._env = environment

    def render_str(self, template: str, data: TemplateData) -> str:
        return self._env.from_string(template).render(**data)

    def render_file(self, template_file: Path, target_file: Path, data: TemplateData) -> None:
        target_file.write_text(self._env.get_template(str(template_file)).render(**data))
