from typing import Any, Mapping, TypeAlias, TypeVar, Callable, Iterable

TemplateData: TypeAlias = Mapping[str, Any]

Item = TypeVar('Item')
LoopOverFn: TypeAlias = Callable[[Iterable[Item]], Item]
RenderFn: TypeAlias = Callable[[str, str, TemplateData], None]
