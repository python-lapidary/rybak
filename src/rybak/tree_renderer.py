from collections.abc import Iterable
from functools import cached_property
from importlib.abc import Traversable
import logging
from pathlib import Path
from typing import Any

from ._types import TemplateData
from .loop import LoopContext, loop_over
from .renderer import Renderer

logger = logging.getLogger(__name__)


class TreeRenderer:
    def __init__(
            self,
            template_root: Traversable,
            target_root: Path,
            renderer: Renderer,
            template_path: Traversable = Path(),
            target_path: Path = Path(),
            *,
            excluded: Iterable[Path] | Iterable[str] = (),
    ) -> None:
        if not template_root.is_dir():
            raise TypeError('template_root must exist and be a directory', template_root)

        self._template_root = template_root
        self._target_root = target_root
        self._renderer = renderer
        self._excluded = tuple(Path(i) for i in excluded)

        self._template_path = template_path
        self._target_path = target_path

    def render(self, data: Any):
        for child in self._full_template_path.iterdir():
            self._render(child.name, data)

    def _render(self, file_name: str, data) -> None:
        """Dispatcher method that calls another render method depending on whether the path is a directory or a file"""

        rel_path = self._template_path / file_name
        if rel_path in self._excluded:
            logger.debug('Excluded %s', rel_path)
            return

        path = self._template_root / str(rel_path)
        if path.is_dir():
            self._render_all_dirs(file_name, data)
        else:
            self._render_all_files(file_name, data)

    def _render_all_dirs(self, file_name: str, data: Any):
        """Create one or more directories from a single template (sub)directory"""
        template_path = self._template_path / file_name
        logger.debug('Render from dir %s', template_path)

        try:
            target_name = self._renderer.render_str(file_name, {
                **data,
            }, loop_over)
            if not target_name:
                logger.info('Skipping, template evaluated to empty value')
            self._render_dir(file_name, target_name, data)
        except LoopContext as loop:
            items = loop.items
        else:
            items = ()

        for item in items:
            target_name = self._renderer.render_str(file_name, {
                **data,
            }, lambda _: item, )
            self._render_dir(file_name, target_name, {**data, 'item': item})

    def _render_dir(self, template_name: str, target_name: str, data: dict[str, Any]):
        """Make sure output directory exists and render all children of the template (sub)directory"""
        logger.debug('Render to dir %s', self._target_path / target_name)

        target_path = self._full_target_path / target_name

        if target_path.exists() and not target_path.is_dir():
            target_path.unlink()
        target_path.mkdir(exist_ok=True)

        self._with_subdir(template_name, target_name).render(data)

    def _render_all_files(self, template_name: str, data: TemplateData):
        """Render one or more files from a single template file"""
        template_path = self._template_path / template_name
        logger.debug('Render from file %s', template_path)

        try:
            target_name = self._renderer.render_str(template_name, {
                **data,
            }, loop_over)
            if not target_name:
                logger.info('Skipping, template evaluated to empty value')
                return
            self._render_file(template_name, target_name, data)
        except LoopContext as loop:
            items = loop.items
        else:
            items = ()

        for item in items:
            target_name = self._renderer.render_str(template_name, {
                **data,
            }, lambda _: item, )
            self._render_file(template_name, target_name, {**data, 'item': item})

    def _render_file(self, template_name: str, target_name: str, data: TemplateData) -> None:
        logger.debug('Render to file %s', self._target_path / target_name)
        target_path = self._full_target_path / target_name
        target_path.parent.mkdir(parents=True, exist_ok=True)
        self._renderer.render_file(
            self._template_path / template_name,
            target_path,
            data,
        )

    def _with_subdir(self, template_name, target_name: str) -> 'TreeRenderer':
        return TreeRenderer(
            self._template_root,
            self._target_root,
            self._renderer,
            self._template_path / template_name,
            self._target_path / target_name,
            excluded=self._excluded,
        )

    @cached_property
    def _full_template_path(self) -> Traversable:
        return self._template_root / str(self._template_path)

    @cached_property
    def _full_target_path(self) -> Path:
        return self._target_root / self._target_path
