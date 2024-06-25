__all__ = [
    'MakoAdapter',
]

import functools
from pathlib import Path
from typing import Optional

import mako.exceptions  # type: ignore[import-untyped]
import mako.lookup
import mako.template

from ._types import LoopOverFn, TemplateData
from .adapter import RendererAdapter, RenderError
from .pycompat import Traversable


class MakoAdapter(RendererAdapter):
    def __init__(self, template_root: Path) -> None:
        self._loader = mako.lookup.TemplateLookup((template_root,))

    def render_str(self, template: str, data: TemplateData, loop_over: Optional[LoopOverFn] = None) -> str:
        try:
            template_obj = str_template(template)
            return template_obj.render(**data, loop_over=loop_over)
        except (AttributeError, mako.exceptions.MakoException, ValueError, TypeError) as e:
            raise RenderError(template) from e

    def render_file(self, template_path: str, data: TemplateData) -> str:
        try:
            template = self._loader.get_template(template_path)
            return template.render(**data)
        except (AttributeError, mako.exceptions.MakoException, ValueError) as e:
            raise RenderError(template_path) from e

    @property
    def template_root(self) -> Traversable:
        paths = self._loader.directories
        if len(paths) != 1:
            raise ValueError('Template root path must be a single path')
        return Path(paths[0])


@functools.lru_cache(maxsize=10)
def str_template(text: str) -> mako.template.Template:
    return mako.template.Template(text)  # noqa: S702
