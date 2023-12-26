__all__ = [
    'TornadoRenderer',
]

import functools
from importlib.resources.abc import Traversable
from pathlib import Path

import tornado.template

from ._types import LoopOverFn, TemplateData
from .renderer import Renderer


class TornadoRenderer(Renderer):
    def __init__(self, template_root: Path) -> None:
        self._loader = tornado.template.Loader(str(template_root))

    def render_str(self, template: str, data: TemplateData, loop_over: LoopOverFn | None = None) -> str:
        template = self.str_template(template)
        return template.generate(**data, loop_over=loop_over).decode('UTF-8')

    def render_file(self, template_path: Traversable, target_file: Path, data: TemplateData) -> None:
        template = self._loader.load(str(template_path))
        text = template.generate(**data)
        target_file.write_bytes(text)

    @functools.lru_cache(maxsize=10)
    def str_template(self, text: str) -> tornado.template.Template:
        return tornado.template.Template(text, loader=self._loader, autoescape=None)
