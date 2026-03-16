from pathlib import Path

from models.data_models import InterfaceDefinition


def parse_syscall_tbl(path: str | Path) -> list[InterfaceDefinition]:
    results: list[InterfaceDefinition] = []
    p = Path(path)
    if not p.exists():
        return results
    for raw in p.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 4:
            results.append(InterfaceDefinition(name=parts[3], source="syscall.tbl"))
    return results
