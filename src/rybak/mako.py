__all__ = [
    'MakoRenderer',
]

import functools
from importlib.resources.abc import Traversable
from pathlib import Path

import mako.template
import mako.lookup

from ._types import LoopOverFn, TemplateData
from .renderer import Renderer


class MakoRenderer(Renderer):
    def __init__(self, template_root: Path) -> None:
        self._loader = mako.lookup.TemplateLookup((template_root,))

    def render_str(self, template: str, data: TemplateData, loop_over: LoopOverFn | None = None) -> str:
        template = self.str_template(template)
        return template.render(**data, loop_over=loop_over)

    def render_file(self, template_path: Traversable, target_file: Path, data: TemplateData) -> None:
        template = self._loader.get_template(str(template_path))
        text = template.render(**data)
        target_file.write_text(text)

    @functools.lru_cache(maxsize=10)
    def str_template(self, text: str) -> mako.template.Template:
        return mako.template.Template(text)
