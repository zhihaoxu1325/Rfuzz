from pathlib import Path


def parse_enabled_devices(path: str | Path) -> set[str]:
    p = Path(path)
    if not p.exists():
        return set()
    devices: set[str] = set()
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "compatible" in line and '"' in line:
            devices.add(line.split('"')[1])
    return devices
