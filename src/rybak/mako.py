__all__ = [
    'MakoAdapter',
]

import functools
from importlib.resources.abc import Traversable
from pathlib import Path

import mako.lookup
import mako.template

from ._types import LoopOverFn, TemplateData
from .adapter import RendererAdapter


class MakoAdapter(RendererAdapter):
    def __init__(self, template_root: Path) -> None:
        self._loader = mako.lookup.TemplateLookup((template_root,))

    def render_str(self, template: str, data: TemplateData, loop_over: LoopOverFn | None = None) -> str:
        template = str_template(template)
        return template.render(**data, loop_over=loop_over)

    def render_file(self, template_path: Traversable, target_file: Path, data: TemplateData) -> None:
        template = self._loader.get_template(str(template_path))
        text = template.render(**data)
        target_file.write_text(text)


@functools.lru_cache(maxsize=10)
def str_template(text: str) -> mako.template.Template:
    return mako.template.Template(text)  # noqa: S702
