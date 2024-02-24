__all__ = [
    'EventSink',
    'LoggingEventSink',
    'RenderError',
    'TreeRenderer',
    'render',
]

from itertools import chain
from pathlib import Path, PurePath
from typing import Iterable, Union, cast

from ._types import RenderError, TemplateData
from .adapter import RendererAdapter
from .events import EventSink, LoggingEventSink
from .tree_renderer import RenderContext, TreeRenderer

_noop_event_sink = EventSink()


def render(
    adapter: RendererAdapter,
    data: TemplateData,
    target_root: Path,
    *,
    exclude: Union[Iterable[Path], Iterable[str]] = ('__pycache__',),
    exclude_extend: Union[Iterable[Path], Iterable[str]] = (),
    remove_stale: bool = False,
    remove_suffixes: Iterable[str] = (),
    event_sink: EventSink = _noop_event_sink,
) -> None:
    """Render a directory-tree from a template and a data dictionary

    :param target_root: render target root directory (filesystem)
    :param adapter: template engine adapter (jinja, mako)
    :param data: template data
    :param exclude: paths within the template root directory, which are not templates. Defaults to '__pycache__'
    :param exclude_extend: paths to be added to the default exclude list.
    :param remove_stale: remove files and directories that were found in the target directory, but not rendered in this
           run.
    :param remove_suffixes: filename suffixes to be removed when rendering file names, in `.suffix` format
    :param event_sink: called when writing or removing files
    """
    exclude_paths = {Path(path) for path in cast(Iterable[Path], chain(exclude, exclude_extend))}
    tree_renderer = TreeRenderer(
        RenderContext(
            adapter=adapter,
            target_root=target_root,
            exclude=exclude_paths,
            remove_suffixes=remove_suffixes,
            event_sink=event_sink,
        ),
        PurePath(),
        Path(),
    )
    tree_renderer.render(data)

    if remove_stale:
        tree_renderer.remove_stale()
