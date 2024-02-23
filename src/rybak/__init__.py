__all__ = [
    'RenderError',
    'TreeRenderer',
    'render',
]

from itertools import chain
from pathlib import Path, PurePath
from typing import Any, Iterable, Union

from ._types import RenderError, ReportCallbackFn, TemplateData
from .adapter import RendererAdapter
from .tree_renderer import RenderContext, TreeRenderer


def _noop_report_cb(*_: Any) -> None:
    pass


def render(
    adapter: RendererAdapter,
    data: TemplateData,
    target_root: Path,
    *,
    exclude: Union[Iterable[Path], Iterable[str]] = ('__pycache__',),
    exclude_extend: Union[Iterable[Path], Iterable[str]] = (),
    remove_suffixes: Iterable[str] = (),
    report_cb: ReportCallbackFn = _noop_report_cb,
) -> None:
    """Render a directory-tree from a template and a data dictionary

    :param target_root: render target root directory (filesystem)
    :param adapter: template engine adapter (jinja, mako)
    :param data: template data
    :param exclude: paths within the template root directory, which are not templates. Defaults to '__pycache__'
    :param exclude_extend: paths to be added to the default exclude list.
    :param remove_suffixes: filename suffixes to be removed when rendering file names, in `.suffix` format
    :param report_cb: callback function called with source and target paths for every written file
    """
    exclude_paths = {Path(path) for path in chain(exclude, exclude_extend)}
    TreeRenderer(
        RenderContext(
            adapter=adapter,
            target_root=target_root,
            exclude=exclude_paths,
            remove_suffixes=remove_suffixes,
            report_cb=report_cb,
        ),
        PurePath(),
        Path(),
    ).render(data)
