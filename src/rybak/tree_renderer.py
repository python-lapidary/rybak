import dataclasses
import logging
import os.path
from functools import cached_property
from pathlib import Path, PurePath
from typing import Iterable, NoReturn

from ._types import LoopOverFn, RenderFn, TemplateData
from .adapter import RendererAdapter
from .pycompat import Traversable

logger = logging.getLogger(__name__)


class StartIteration(Exception):  # noqa: N818
    """
    Helper exception for loop_over template function. When raised, renderer will iterate over the items.
    Deliberately named after StopIteration.
    """

    def __init__(self, items: Iterable) -> None:
        self.items = items


def loop_over(items: Iterable) -> NoReturn:
    if isinstance(items, str):
        raise TypeError('Expected an Iterable other than str')
    if not isinstance(items, Iterable):
        raise TypeError('Expected an Iterable')
    raise StartIteration(items)


@dataclasses.dataclass
class RenderContext:
    target_root: Path
    adapter: RendererAdapter
    exclude: Iterable[PurePath]
    remove_suffixes: Iterable[str]


class TreeRenderer:
    def __init__(self, context: RenderContext, template_path: PurePath, target_path: Path) -> None:
        self._context = context
        self._template_path = template_path
        self._target_path = target_path

    def render(self, data: TemplateData):
        for child in self._full_template_path.iterdir():
            self._render(child.name, data)

    def _render(self, file_name: str, data: TemplateData) -> None:
        """Dispatcher method that calls another render method depending on whether the path is a directory or a file"""

        rel_path = self._template_path / file_name
        if rel_path in self._context.exclude:
            logger.debug('Excluded %s', rel_path)
            return

        path = self._context.adapter.template_root / rel_path
        if path.is_dir():
            render_single = self._render_dir
        else:
            render_single = self._render_file

        self._render_all(file_name, data, render_single)

    def _render_all(self, template_name: str, data: TemplateData, render_single: RenderFn):
        template_path = self._template_path / template_name
        logger.debug('Render from %s', template_path)

        try:
            target_name = self._render_file_name(template_name, data, loop_over)
            if not target_name:
                logger.info('Skipping, template file name evaluated to empty value')
                return
            render_single(template_name, target_name, data)
        except StartIteration as e:
            items = e.items
        else:
            items = ()

        for item in items:
            target_name = self._render_file_name(template_name, data, lambda _: item)  # noqa: B023
            if not target_name:
                logger.info('Skipping, template file name evaluated to empty value')
                continue
            render_single(template_name, target_name, {**data, 'item': item})

    def _render_dir(self, template_name: str, target_name: str, data: TemplateData):
        """Make sure output directory exists and render all children of the template (sub)directory"""
        logger.debug('Render to dir %s', self._target_path / target_name)

        target_path = self._full_target_path / target_name

        if target_path.exists() and not target_path.is_dir():
            target_path.unlink()
        target_path.mkdir(exist_ok=True)

        self._with_subdir(template_name, target_name).render(data)

    def _render_file_name(self, template: str, data: TemplateData, loop_over_: LoopOverFn) -> str:
        if self._context.remove_suffixes:
            root, ext = os.path.splitext(template)
            if ext in self._context.remove_suffixes:
                template = root
        target_name = self._context.adapter.render_str(
            template,
            data,
            loop_over_,
        )
        return target_name

    def _render_file(self, template_name: str, target_name: str, data: TemplateData) -> None:
        logger.debug('Render to file %s', self._target_path / target_name)
        target_path = self._full_target_path / target_name
        target_path.parent.mkdir(parents=True, exist_ok=True)
        self._context.adapter.render_file(
            (self._template_path / template_name).as_posix(),
            target_path,
            data,
        )

    def _with_subdir(self, template_name: str, target_name: str) -> 'TreeRenderer':
        return TreeRenderer(self._context, self._template_path / template_name, self._target_path / target_name)

    @cached_property
    def _full_template_path(self) -> Traversable:
        return self._context.adapter.template_root / str(self._template_path)

    @cached_property
    def _full_target_path(self) -> Path:
        return self._context.target_root / self._target_path
