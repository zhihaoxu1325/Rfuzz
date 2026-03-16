from pathlib import Path


def save_seed(path: str | Path, interface: str, dsl: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)
    Path(path, f"{interface}.syz").write_text(dsl + "\n", encoding="utf-8")
