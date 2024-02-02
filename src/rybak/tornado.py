__all__ = [
    'TornadoAdapter',
]

from pathlib import Path
from typing import Optional

import tornado.template

from ._types import LoopOverFn, TemplateData
from .adapter import RendererAdapter
from .pycompat import Traversable


class TornadoAdapter(RendererAdapter):
    def __init__(self, template_root: Path) -> None:
        self._loader = tornado.template.Loader(str(template_root))

    def render_str(self, template: str, data: TemplateData, loop_over: Optional[LoopOverFn] = None) -> str:
        template_obj = self.str_template(template)
        return template_obj.generate(**data, loop_over=loop_over).decode('UTF-8')

    def render_file(self, template_path: Traversable, target_file: Path, data: TemplateData) -> None:
        template = self._loader.load(str(template_path))
        text = template.generate(**data)
        target_file.write_bytes(text)

    def str_template(self, text: str) -> tornado.template.Template:
        return tornado.template.Template(text, loader=self._loader, autoescape=None)
