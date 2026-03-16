from pathlib import Path
import re

COMPAT_RE = re.compile(r'compatible\s*=\s*"([^"]+)"')
STATUS_RE = re.compile(r'status\s*=\s*"([^"]+)"')


def parse_enabled_devices(path: str | Path) -> set[str]:
    p = Path(path)
    if not p.exists():
        return set()

    enabled: set[str] = set()
    current_compat: str | None = None
    current_enabled = True

    for raw in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        compat_match = COMPAT_RE.search(line)
        if compat_match:
            current_compat = compat_match.group(1)
            current_enabled = True

        status_match = STATUS_RE.search(line)
        if status_match:
            current_enabled = status_match.group(1) not in {"disabled", "fail"}

        if line.endswith(";") and current_compat:
            if current_enabled:
                enabled.add(current_compat)
            current_compat = None
            current_enabled = True

    return enabled
