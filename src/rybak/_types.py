from collections.abc import Callable, Iterable
from typing import Any, Mapping, TypeAlias, TypeVar

TemplateData: TypeAlias = Mapping[str, Any]

Item = TypeVar('Item')
LoopOverFn: TypeAlias = Callable[[Iterable[Item]], Item]
