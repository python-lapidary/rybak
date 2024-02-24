__all__ = [
    'EventSink',
    'LoggingEventSink',
    'RenderError',
    'TreeTemplate',
    'render',
]

from pathlib import Path
from typing import Container, Iterable, Union

from typing_extensions import deprecated

from ._types import TemplateData
from .adapter import RendererAdapter, RenderError
from .events import EventSink, LoggingEventSink
from .tree_renderer import TreeTemplate, _noop_event_sink


@deprecated('For removal in 0.4. Use TreeTemplate.render')
def render(
    adapter: RendererAdapter,
    data: TemplateData,
    target_root: Path,
    *,
    exclude: Union[Iterable[Path], Iterable[str]] = ('__pycache__',),
    exclude_extend: Union[Iterable[Path], Iterable[str]] = (),
    remove_stale: bool = False,
    remove_suffixes: Container[str] = (),
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

    template = TreeTemplate(
        adapter,
        remove_suffixes=remove_suffixes,
        exclude=exclude,
        exclude_extend=exclude_extend,
    )
    template.render(data, target_root, event_sink=event_sink, remove_stale=remove_stale)
