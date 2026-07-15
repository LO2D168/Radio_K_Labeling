"""Command-line entry point for inspecting instances."""

import argparse

from .io.mtx import read_mtx_to_adj


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect a radio k-labeling Matrix Market graph")
    parser.add_argument("path", help="path to a Matrix Market adjacency matrix")
    args = parser.parse_args()
    vertices, edges, _ = read_mtx_to_adj(args.path)
    print(f"vertices={vertices} edges={edges}")
