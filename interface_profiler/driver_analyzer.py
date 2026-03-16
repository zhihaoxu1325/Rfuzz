from pathlib import Path
import re


IOCTL_RE = re.compile(r"\b(_IO|_IOR|_IOW|_IOWR)\s*\(")


def extract_ioctl_files(root: str | Path) -> list[str]:
    found: list[str] = []
    for p in Path(root).glob("**/*.[ch]"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        if IOCTL_RE.search(text):
            found.append(str(p))
    return found
