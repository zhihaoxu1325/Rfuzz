from pathlib import Path


def save_seed(path: str | Path, interface: str, dsl: str, suffix: str = "") -> Path:
    out_dir = Path(path)
    out_dir.mkdir(parents=True, exist_ok=True)
    name = f"{interface}{suffix}.syz"
    out_path = out_dir / name
    out_path.write_text(dsl + "\n", encoding="utf-8")
    return out_path
