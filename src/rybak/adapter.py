import abc
from importlib.resources.abc import Traversable
from pathlib import Path
from typing import Any

from ._types import LoopOverFn, TemplateData


class RendererAdapter(abc.ABC):
    @abc.abstractmethod
    def __init__(self, **kwargs: Any) -> None:
        pass

    @abc.abstractmethod
    def render_str(self, template: str, data: TemplateData, loop_over: LoopOverFn) -> str:
        pass

    @abc.abstractmethod
    def render_file(self, template_file: Traversable, target_file: Path, data: TemplateData) -> None:
        pass
