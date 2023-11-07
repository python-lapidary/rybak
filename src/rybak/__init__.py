__all__ = [
    'render',
    'TreeRenderer',
]

from pathlib import Path

from ._types import TemplateData
from .loop import LoopContext, loop_over
from .renderer import RendererFactory
from .tree_renderer import TreeRenderer


def render(template_root: Path, target_root: Path, renderer_factory: RendererFactory, data: TemplateData) -> None:
    TreeRenderer(template_root, target_root, renderer_factory(template_root)).render(data)
