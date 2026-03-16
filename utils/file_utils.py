from pathlib import Path
from typing import Iterable


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def write_lines(path: str | Path, lines: Iterable[str]) -> None:
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
