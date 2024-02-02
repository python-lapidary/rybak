from pathlib import Path
from typing import Any, Optional

import jinja2

from ._types import LoopOverFn, RenderError, TemplateData
from .adapter import RendererAdapter
from .pycompat import Traversable


class JinjaAdapter(RendererAdapter):
    """Adapter for Jinja engine.
    Unless you pass your own jinja.Environment instance, the default for keep_trailing_newline is True."""

    def __init__(self, environment: Optional[jinja2.Environment] = None, **env_kwargs: Any) -> None:
        keep_trailing_newline = env_kwargs.pop('keep_trailing_newline', True)
        self._env = environment or jinja2.Environment(
            keep_trailing_newline=keep_trailing_newline,
            **env_kwargs,
        )

    def render_str(self, template: str, data: TemplateData, loop_over: Optional[LoopOverFn] = None) -> str:
        env = self._env.overlay()
        env.globals['loop_over'] = loop_over

        template_obj = env.from_string(template)
        try:
            return template_obj.render(**data)
        except jinja2.TemplateError as e:
            raise RenderError from e

    def render_file(self, template_file: Traversable, target_file: Path, data: TemplateData) -> None:
        template_obj = self._env.get_template(str(template_file))
        try:
            text = template_obj.render(**data)
        except jinja2.TemplateError as e:
            raise RenderError from e
        target_file.write_text(text)
