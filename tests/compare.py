from pathlib import Path
from typing import Iterable, Optional, Tuple


def dir_content(root: Path) -> Iterable[Tuple[str, Optional[str]]]:
    return sorted(
        (path.relative_to(root).as_posix(), path.read_text() if path.is_file() else None) for path in root.rglob('*')
    )
