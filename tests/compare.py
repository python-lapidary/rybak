from collections.abc import Iterable
from pathlib import Path
from typing import Optional


def dir_content(root: Path) -> Iterable[tuple[str, Optional[str]]]:
    return sorted(
        (str(path.relative_to(root)), path.read_text() if path.is_file() else None) for path in root.rglob('*')
    )
