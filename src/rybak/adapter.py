import abc
from pathlib import Path
from typing import Any

from ._types import LoopOverFn, TemplateData
from .pycompat import Traversable


class RendererAdapter(abc.ABC):
    @abc.abstractmethod
    def __init__(self, **kwargs: Any) -> None:
        pass

    @abc.abstractmethod
    def render_str(self, template: str, data: TemplateData, loop_over: LoopOverFn) -> str:
        pass

    @abc.abstractmethod
    def render_file(self, template_path: str, target_file: Path, data: TemplateData) -> None:
        pass

    @property
    @abc.abstractmethod
    def template_root(self) -> Traversable:
        pass
