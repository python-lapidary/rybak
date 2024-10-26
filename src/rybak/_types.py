from collections.abc import Iterable, Mapping
from pathlib import PurePath
from typing import Any, Callable, TypeVar

from .pycompat import TypeAlias

TemplateData: TypeAlias = Mapping[str, Any]

Item = TypeVar('Item')
LoopOverFn: TypeAlias = Callable[[Iterable[Item]], Item]
ConflictHandler: TypeAlias = Callable[[PurePath, PurePath], bool]
