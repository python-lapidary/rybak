__all__ = [
    'RenderError',
    'TreeRenderer',
    'render',
]

from pathlib import Path, PurePath
from typing import Iterable, Union

from ._types import RenderError, TemplateData
from .adapter import RendererAdapter
from .tree_renderer import RenderContext, TreeRenderer


def render(
    adapter: RendererAdapter,
    data: TemplateData,
    target_root: Path,
    *,
    excluded: Union[Iterable[Path], Iterable[str]] = (),
    remove_suffixes: Iterable[str] = (),
) -> None:
    """Render a directory-tree from a template and a data dictionary

    :param target_root: render target root directory (filesystem)
    :param adapter: template engine adapter (jinja, mako)
    :param data: template data
    :param excluded: paths within the template root directory, which are not templates
    :param remove_suffixes: filename suffixes to be removed when rendering file names, in `.suffix` format
    """
    exclude_paths = {Path(path) for path in excluded}
    TreeRenderer(
        RenderContext(
            adapter=adapter,
            target_root=target_root,
            excluded=exclude_paths,
            remove_suffixes=remove_suffixes,
        ),
        PurePath(),
        Path(),
    ).render(data)
