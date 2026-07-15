"""Stable result serialization helpers."""

from pathlib import Path

import pandas as pd


def write_results(rows: list[dict], output: str | Path) -> None:
    """Write result rows without relying on the process current directory."""
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output_path, index=False)
