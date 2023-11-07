__all__ = [
    'render',
    'TreeRenderer',
]

from collections.abc import Iterable
from pathlib import Path
from typing import Any

from ._types import TemplateData
from .loop import LoopContext, loop_over
from .renderer import Renderer, RendererFactory
from .tree_renderer import TreeRenderer


def render(
        template_root: Path,
        target_root: Path,
        renderer: type[Renderer] | Renderer,
        data: TemplateData,
        *,
        renderer_args: dict[str, Any] | None = None,
        excluded: Iterable[Path] = (),
) -> None:
    actual_renderer = (
        renderer
        if isinstance(renderer, Renderer)
        else renderer(template_root=template_root, **renderer_args if renderer_args else {})
    )

    TreeRenderer(
        template_root,
        target_root,
        actual_renderer,
        excluded=excluded,
    ).render(data)
