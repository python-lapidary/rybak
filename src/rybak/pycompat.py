__all__ = (
    'Traversable',
    'TypeAlias',
    'files',
)

import sys

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias


if sys.version_info >= (3, 12):
    from importlib.resources import files
    from importlib.resources.abc import Traversable
else:
    from importlib_resources import files  # type: ignore[import-not-found]
    from importlib_resources.abc import Traversable  # type: ignore[import-not-found]
