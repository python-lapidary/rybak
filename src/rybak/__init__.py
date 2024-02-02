__all__ = [
    'render',
    'TreeRenderer',
]

from collections.abc import Iterable
from importlib.abc import Traversable
from pathlib import Path
from typing import Any

from ._types import TemplateData
from .renderer import Renderer
from .tree_renderer import TreeRenderer


def render(
        template_root: Traversable,
        target_root: Path,
        renderer_: type[Renderer] | Renderer,
        data: TemplateData,
        *,
        renderer_args: dict[str, Any] | None = None,
        excluded: Iterable[Path] = (),
        remove_suffixes: Iterable[str] = (),
) -> None:
    """

    :param template_root: root template directory (filesystem or importlib resource)
    :param target_root: render target root directory (filesystem)
    :param renderer_: template engine adapter (jinja, mako, tornado) or its type
    :param data: template data
    :param renderer_args: parameters for template engine adapter, when just the adapter class is passed
    :param excluded: paths within the template root directory, which are not templates
    :param remove_suffixes: template filename suffixes to be removed when rendering file names, in `.suffix` format
    """
    actual_renderer = (
        renderer_
        if isinstance(renderer_, Renderer)
        else renderer_(template_root=template_root, **renderer_args if renderer_args else {})
    )

    TreeRenderer(
        template_root,
        target_root,
        actual_renderer,
        excluded=excluded,
        remove_suffixes=remove_suffixes,
    ).render(data)
