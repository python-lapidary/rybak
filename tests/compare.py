from pathlib import Path
from typing import Iterable, Optional, Tuple


def dir_content(root: Path) -> Iterable[Tuple[str, Optional[str]]]:
    return sorted(
        (str(path.relative_to(root)), path.read_text() if path.is_file() else None) for path in root.rglob('*')
    )
