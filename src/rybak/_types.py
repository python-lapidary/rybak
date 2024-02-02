from typing import Any, Callable, Iterable, Mapping, TypeAlias, TypeVar

TemplateData: TypeAlias = Mapping[str, Any]

Item = TypeVar('Item')
LoopOverFn: TypeAlias = Callable[[Iterable[Item]], Item]
RenderFn: TypeAlias = Callable[[str, str, TemplateData], None]
