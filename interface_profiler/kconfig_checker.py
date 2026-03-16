from pathlib import Path


def parse_kconfig(path: str | Path) -> dict[str, str]:
    cfg: dict[str, str] = {}
    p = Path(path)
    if not p.exists():
        return cfg
    for raw in p.read_text(encoding="utf-8").splitlines():
        if raw.startswith("CONFIG_") and "=" in raw:
            k, v = raw.split("=", 1)
            cfg[k] = v
    return cfg
