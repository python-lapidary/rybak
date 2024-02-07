__all__ = [
    'MakoAdapter',
]

import functools
from pathlib import Path
from typing import Optional

import mako.exceptions
import mako.lookup
import mako.template

from ._types import LoopOverFn, RenderError, TemplateData
from .adapter import RendererAdapter


class MakoAdapter(RendererAdapter):
    def __init__(self, template_root: Path) -> None:
        self._loader = mako.lookup.TemplateLookup((template_root,))

    def render_str(self, template: str, data: TemplateData, loop_over: Optional[LoopOverFn] = None) -> str:
        try:
            template_obj = str_template(template)
            return template_obj.render(**data, loop_over=loop_over)
        except (AttributeError, mako.exceptions.MakoException, ValueError) as e:
            raise RenderError from e

    def render_file(self, template_path: str, target_file: Path, data: TemplateData) -> None:
        try:
            template = self._loader.get_template(template_path)
            text = template.render(**data)
        except (AttributeError, mako.exceptions.MakoException, ValueError) as e:
            raise RenderError from e
        target_file.write_text(text)


@functools.lru_cache(maxsize=10)
def str_template(text: str) -> mako.template.Template:
    return mako.template.Template(text)  # noqa: S702
