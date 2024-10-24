__all__ = [
    'MakoAdapter',
]

import functools
from collections.abc import Iterable
from pathlib import Path
from typing import Optional, cast

import mako.exceptions  # type: ignore[import-untyped]
import mako.lookup
import mako.template

from ._types import LoopOverFn, TemplateData
from .adapter import RendererAdapter, RenderError
from .pycompat import Traversable


class MakoAdapter(RendererAdapter):
    def __init__(self, template_roots: Iterable[Path]) -> None:
        self._loader = mako.lookup.TemplateLookup(list(template_roots))

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
    def template_roots(self) -> Iterable[Traversable]:
        return [cast(Traversable, Path(directory)) for directory in self._loader.directories]


@functools.lru_cache(maxsize=10)
def str_template(text: str) -> mako.template.Template:
    return mako.template.Template(text)  # noqa: S702
