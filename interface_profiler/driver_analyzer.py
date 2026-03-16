from pathlib import Path
import re

from models.data_models import InterfaceDefinition

IOCTL_RE = re.compile(r"\b(_IO|_IOR|_IOW|_IOWR)\s*\(")
COMPAT_RE = re.compile(r"of_device_id\s+\w+\[\]\s*=\s*\{", re.MULTILINE)
STRING_RE = re.compile(r'"([a-zA-Z0-9,._-]+)"')


def parse_driver_interfaces(root: str | Path) -> list[InterfaceDefinition]:
    interfaces: list[InterfaceDefinition] = []
    for p in Path(root).glob("**/*.[ch]"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        if not IOCTL_RE.search(text):
            continue

        device = None
        if COMPAT_RE.search(text):
            candidates = STRING_RE.findall(text)
            device = candidates[0] if candidates else None

        interfaces.append(
            InterfaceDefinition(
                name=f"ioctl@{p.stem}",
                source="driver",
                params=["fd", "cmd", "arg_ptr"],
                bound_device=device,
            )
        )
    return interfaces
