import abc
from collections.abc import Callable
from pathlib import Path
from typing import TypeAlias

from ._types import TemplateData


class Renderer(abc.ABC):
    @abc.abstractmethod
    def render_str(self, template: str, data: TemplateData) -> str:
        pass

    @abc.abstractmethod
    def render_file(self, template_file: Path, target_file: Path, data: TemplateData) -> None:
        pass


RendererFactory: TypeAlias = Callable[[Path], Renderer]
