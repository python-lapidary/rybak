from collections.abc import Iterable
from pathlib import Path
from typing import Optional, cast

import jinja2

from ._types import LoopOverFn, TemplateData
from .adapter import RendererAdapter, RenderError
from .pycompat import Traversable, files


class JinjaAdapter(RendererAdapter):
    """Adapter for Jinja engine.
    Unless you pass your own jinja.Environment instance, the default for keep_trailing_newline is True,
    and the default loader is FileSystemLoader."""

    def __init__(
        self,
        environment: Optional[jinja2.Environment] = None,
        loader: Optional[jinja2.BaseLoader] = None,
        keep_trailing_newline: Optional[bool] = True,
    ) -> None:
        """Create adapter for Jinja Environment. Only either `loader` or `environment` is accepted."""

        if environment:
            if loader:
                raise ValueError('Set loader in the Jinja environment')
        elif not loader:
            raise ValueError('Either environment or loader is required')

        if not environment:
            self._env = jinja2.Environment(loader=loader, keep_trailing_newline=keep_trailing_newline or True)
        else:
            if keep_trailing_newline is not None:
                self._env = environment.overlay()
                self._env.keep_trailing_newline = keep_trailing_newline

    def render_str(self, template: str, data: TemplateData, loop_over: Optional[LoopOverFn] = None) -> str:
        env = self._env.overlay()
        env.globals['loop_over'] = loop_over

        try:
            template_obj = env.from_string(template)
            return template_obj.render(**data)
        except (jinja2.TemplateError, ValueError) as e:
            raise RenderError(template) from e

    def render_file(self, template_path: str, data: TemplateData) -> str:
        try:
            template_obj = self._env.get_template(template_path)
            return template_obj.render(**data)
        except (jinja2.TemplateError, ValueError) as e:
            raise RenderError(template_path) from e

    @property
    def template_roots(self) -> Iterable[Traversable]:
        yield from _template_roots(self._env.loader)


def _template_roots(loader: jinja2.BaseLoader) -> Iterable[Traversable]:
    if isinstance(loader, jinja2.FileSystemLoader):
        for path in loader.searchpath:
            yield Path(path)
    elif isinstance(loader, jinja2.PackageLoader):
        yield cast(Traversable, files(loader.package_name) / loader.package_path)
    elif isinstance(loader, jinja2.ChoiceLoader):
        for sub_loader in loader.loaders:
            yield from _template_roots(sub_loader)
    else:
        raise TypeError(type(loader))
