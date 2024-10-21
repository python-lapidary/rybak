from collections.abc import Iterable
from pathlib import Path
from typing import Optional


def dir_content(root: Path) -> Iterable[tuple[str, Optional[str]]]:
    return sorted(
        (path.relative_to(root).as_posix(), path.read_text() if path.is_file() else None) for path in root.rglob('*')
    )
