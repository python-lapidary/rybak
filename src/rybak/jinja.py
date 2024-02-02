from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Optional

import jinja2

from ._types import LoopOverFn, TemplateData
from .adapter import RendererAdapter


class JinjaAdapter(RendererAdapter):
    """Adapter for Jinja engine.
    Unless you pass your own jinja.Environment instance, the default for keep_trailing_newline is True."""
    def __init__(
        self,
        environment: Optional[jinja2.Environment] = None,
        **env_kwargs
    ) -> None:
        keep_trailing_newline = env_kwargs.pop('keep_trailing_newline', True)
        self._env = environment or jinja2.Environment(
            keep_trailing_newline=keep_trailing_newline,
            **env_kwargs,
        )

    def render_str(self, template: str, data: TemplateData, loop_over: LoopOverFn | None = None) -> str:
        env = self._env.overlay()
        env.globals['loop_over'] = loop_over

        return env.from_string(template).render(**data)

    def render_file(self, template_file: Traversable, target_file: Path, data: TemplateData) -> None:
        target_file.write_text(self._env.get_template(str(template_file)).render(**data))
