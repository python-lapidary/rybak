import abc

from ._types import LoopOverFn, TemplateData
from .pycompat import Traversable


class RendererAdapter(abc.ABC):
    @abc.abstractmethod
    def render_str(self, template: str, data: TemplateData, loop_over: LoopOverFn) -> str:
        pass

    @abc.abstractmethod
    def render_file(self, template_path: str, data: TemplateData) -> str:
        pass

    @property
    @abc.abstractmethod
    def template_root(self) -> Traversable:
        pass


class RenderError(Exception):
    pass
