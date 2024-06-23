from typing import Any, Callable, Iterable, Mapping, TypeVar

from typing_extensions import TypeAlias

TemplateData: TypeAlias = Mapping[str, Any]

Item = TypeVar('Item')
LoopOverFn: TypeAlias = Callable[[Iterable[Item]], Item]
