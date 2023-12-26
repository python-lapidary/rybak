from pathlib import Path

import jinja2

from ._types import LoopOverFn, TemplateData
from .renderer import Renderer


class JinjaRenderer(Renderer):
    def __init__(self, environment: jinja2.Environment) -> None:
        self._env = environment

    def render_str(self, template: str, data: TemplateData, loop_over: LoopOverFn | None = None) -> str:
        env = self._env.overlay()
        env.globals['loop_over'] = loop_over

    def render_file(self, template_file: Path, target_file: Path, data: TemplateData) -> None:
        return env.from_string(template).render(**data)

        target_file.write_text(self._env.get_template(str(template_file)).render(**data))
