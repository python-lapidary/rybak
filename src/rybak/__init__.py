__all__ = [
    'RenderError',
    'TreeRenderer',
    'render',
]

from pathlib import Path
from typing import Any, Iterable, Mapping, Optional, Type, Union

from ._types import RenderError, TemplateData
from .adapter import RendererAdapter
from .pycompat import Traversable
from .tree_renderer import RenderContext, TreeRenderer


def render(
    template_root: Traversable,
    target_root: Path,
    adapter: Union[Type[RendererAdapter], RendererAdapter],
    data: TemplateData,
    *,
    renderer_args: Optional[Mapping[str, Any]] = None,
    excluded: Iterable[Path] = (),
    remove_suffixes: Iterable[str] = (),
) -> None:
    """Render a directory-tree from a template and a data dictionary

    :param template_root: root template directory (filesystem or importlib resource)
    :param target_root: render target root directory (filesystem)
    :param adapter: template engine adapter (jinja, mako, tornado) or its type
    :param data: template data
    :param renderer_args: parameters for template engine adapter, when just the adapter class is passed
    :param excluded: paths within the template root directory, which are not templates
    :param remove_suffixes: filename suffixes to be removed when rendering file names, in `.suffix` format
    """
    actual_renderer = (
        adapter
        if isinstance(adapter, RendererAdapter)
        else adapter(template_root=template_root, **renderer_args if renderer_args else {})
    )

    TreeRenderer(
        RenderContext(
            template_root=template_root,
            target_root=target_root,
            adapter=actual_renderer,
            excluded=excluded,
            remove_suffixes=remove_suffixes,
        ),
        Path(),
        Path(),
    ).render(data)
