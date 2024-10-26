import dataclasses
import itertools
import logging
import os.path
from collections.abc import Container, Iterable, Iterator, MutableSet
from pathlib import Path, PurePath
from typing import Any, NoReturn, Optional, Union, cast

from ._types import ConflictHandler, LoopOverFn, TemplateData
from .adapter import RendererAdapter, RenderError
from .events import EventSink
from .pycompat import Traversable

logger = logging.getLogger(__name__)

_noop_event_sink = EventSink()


class StartIteration(Exception):  # noqa: N818
    """
    Helper exception for `loop_over` template function. When raised, renderer will iterate over the items.
    Deliberately named after StopIteration.
    """

    def __init__(self, items: Iterable) -> None:
        self.items = items


def loop_over(items: Iterable) -> NoReturn:
    if isinstance(items, str):
        raise TypeError('Expected an Iterable other than str')
    if not isinstance(items, Iterable):
        raise TypeError('Expected an Iterable', type(items))
    raise StartIteration(items)


def _default_conflict_handler(template: PurePath, target: PurePath) -> bool:
    raise RenderError('Conflicting path', template, target)


@dataclasses.dataclass
class RenderContext:
    """Holds context for rendering a single file or directory"""

    template_root: Traversable
    template_path: PurePath
    target_path: PurePath
    session: 'Session'
    data: TemplateData

    def with_child(self, template_name: str, target_name: str, data: Optional[TemplateData]) -> 'RenderContext':
        """Create a child context. Pass on the render session."""
        return RenderContext(
            self.template_root,
            self.template_path / template_name,
            self.target_path / target_name,
            self.session,
            data or self.data,
        )

    def render(self) -> None:
        """Render files and directories in ctx.template_path into ctx.target_path"""

        for child in self.full_template_path.iterdir():
            self._render_child(child.name)

    def _render_child(self, file_name: str) -> None:
        """Dispatcher method that calls another render method depending on whether the path is a directory or a file"""

        rel_path = self.template_path / file_name
        if rel_path in self.session.template._exclude:
            logger.debug('Excluded %s', rel_path)
            return

        logger.debug('Render from %s', rel_path)

        path = self.full_template_path / file_name
        if path.is_dir():
            render_single = RenderContext._render_dir
        else:
            render_single = RenderContext._render_file

        for target_name, item in self.render_names(file_name, self.data):
            data_child = {**self.data, 'item': item} if item else self.data
            render_single(self.with_child(file_name, target_name, data_child))

    def render_names(self, template_name: str, data: TemplateData) -> Iterator[tuple[str, Any]]:
        """Produce zero or more target names for a given template file name"""

        try:
            target_name = self.session.template._render_file_name(template_name, data, loop_over)
            if not target_name:
                logger.info('Skipping, template file name evaluated to empty value')
                return
            yield target_name, None
        except StartIteration as e:
            items = e.items
        else:
            items = ()

        for item in items:
            target_name = self.session.template._render_file_name(template_name, data, lambda _: item)  # noqa: B023
            if not target_name:
                logger.info('Skipping, template file name evaluated to empty value')
                continue
            yield target_name, item

    def _render_dir(self) -> None:
        """Make sure output directory exists and render all children of the template (sub)directory"""
        logger.debug('Render to dir %s', self.target_path)

        target_path = self.full_target_path
        if target_path.exists() and not target_path.is_dir():
            target_path.unlink()

        self.render()

    def _render_file(self) -> None:
        if self.target_path in self.session.files_written:
            if not self.session.conflict_handler(self.template_path, self.target_path):
                logger.debug('Not rendering to file %s due to a conflict.', self.target_path)

        logger.debug('Render to file %s', self.target_path)
        self.session.writing_file(self.template_path, self.target_path)
        self.session.template._render_file(self.template_path, self.full_target_path, self.data)

    @property
    def full_target_path(self) -> Path:
        return self.session.target_root / self.target_path

    @property
    def full_template_path(self) -> Traversable:
        return self.template_root / str(self.template_path)


class TreeTemplate:
    def __init__(
        self,
        adapter: RendererAdapter,
        *,
        remove_suffixes: Container[str] = (),
        exclude: Union[Iterable[str], Iterable[PurePath]] = ('__pycache__',),
        exclude_extend: Union[Iterable[str], Iterable[PurePath]] = (),
        on_conflict: ConflictHandler = _default_conflict_handler,
    ) -> None:
        self._adapter = adapter
        self._remove_suffixes = remove_suffixes
        self._exclude = [
            PurePath(cast(Union[str, PurePath], path)) for path in itertools.chain(exclude, exclude_extend)
        ]
        self._on_conflict = on_conflict

    def render(
        self,
        data: TemplateData,
        target_root: Path,
        *,
        event_sink: EventSink = _noop_event_sink,
        remove_stale: bool = False,
    ) -> None:
        session = Session(self, target_root, event_sink, self._on_conflict)
        for template_root in self._adapter.template_roots:
            ctx = RenderContext(
                template_root,
                PurePath(),
                PurePath(),
                session,
                data,
            )
            ctx.render()

        # Removing stale files is done at the end since rendered file names can be whole paths, so it's hard to say
        # that a given file will not be rendered or directory will end up empty until all template files has been
        # processed
        if remove_stale:
            session.remove_stale()

    def _render_file_name(self, template: str, data: TemplateData, loop_over: LoopOverFn) -> str:
        if self._remove_suffixes:
            root, suffix = os.path.splitext(template)
            if suffix in self._remove_suffixes:
                template = root
        return self._adapter.render_str(
            template,
            data,
            loop_over,
        )

    def _render_file(self, template_path: PurePath, target_path: Path, data: TemplateData) -> None:
        target_path.parent.mkdir(parents=True, exist_ok=True)

        text = self._adapter.render_file(template_path.as_posix(), data)
        target_path.write_text(text)


@dataclasses.dataclass
class Session:
    template: 'TreeTemplate'
    target_root: Path
    event_sink: EventSink
    conflict_handler: ConflictHandler
    files_written: MutableSet[PurePath] = dataclasses.field(default_factory=set)

    def remove_stale(self) -> None:
        for path_, dirs, files in os.walk(self.target_root, False):
            path = Path(path_)
            existing_dir_path = PurePath(path.relative_to(self.target_root))
            removed_files: MutableSet[str] = set()

            for file_name in files:
                file_path = existing_dir_path / file_name

                if file_path not in self.files_written:
                    self.event_sink.unlinking_file(file_path)
                    removed_files.add(file_name)
                    (self.target_root / file_path).unlink()

            if path != self.target_root and not dirs and set(files) == removed_files:
                self.event_sink.unlinking_file(path)
                path.rmdir()

    def writing_file(self, template: PurePath, target: PurePath) -> None:
        self.files_written.add(target)
        self.event_sink.writing_file(template, target)
