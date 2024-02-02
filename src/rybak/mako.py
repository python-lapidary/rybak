__all__ = [
    'MakoAdapter',
]

import functools
from pathlib import Path
from typing import Optional

import mako.lookup
import mako.template

from ._types import LoopOverFn, TemplateData
from .adapter import RendererAdapter
from .pycompat import Traversable


class MakoAdapter(RendererAdapter):
    def __init__(self, template_root: Path) -> None:
        self._loader = mako.lookup.TemplateLookup((template_root,))

    def render_str(self, template: str, data: TemplateData, loop_over: Optional[LoopOverFn] = None) -> str:
        template_obj = str_template(template)
        return template_obj.render(**data, loop_over=loop_over)

    def render_file(self, template_path: Traversable, target_file: Path, data: TemplateData) -> None:
        template = self._loader.get_template(str(template_path))
        text = template.render(**data)
        target_file.write_text(text)


@functools.lru_cache(maxsize=10)
def str_template(text: str) -> mako.template.Template:
    return mako.template.Template(text)  # noqa: S702
