__all__ = [
    'Traversable',
    'TypeAlias',
]

import sys

if sys.version_info >= (3, 12):
    from importlib.resources.abc import Traversable
else:
    from importlib_resources.abc import Traversable

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias