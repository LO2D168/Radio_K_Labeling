#!/usr/bin/env python3
"""Validate and summarize Matrix Market graph instances."""

import argparse

from radio_k_labeling.io.mtx import read_mtx_to_adj


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="Matrix Market files")
    args = parser.parse_args()
    for path in args.paths:
        vertices, edges, _ = read_mtx_to_adj(path)
        print(f"{path}: vertices={vertices} edges={edges}")


if __name__ == "__main__":
    main()
