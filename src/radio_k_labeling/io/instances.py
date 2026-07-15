"""Deterministic discovery of Matrix Market instances."""

from pathlib import Path


def list_instances(dataset_dir: str | Path) -> list[Path]:
    """Return dataset files in lexical order without changing their names."""
    return sorted(Path(dataset_dir).glob("*.mtx"))
