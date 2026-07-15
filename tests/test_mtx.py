from pathlib import Path

import numpy as np
from scipy.io import mmwrite

from radio_k_labeling.io.mtx import read_mtx_to_adj


def test_matrix_market_round_trip(tmp_path: Path):
    path = tmp_path / "path_P3.mtx"
    matrix = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    mmwrite(path, matrix)
    vertices, edges, adjacency = read_mtx_to_adj(path)
    assert (vertices, edges) == (3, 2)
    assert adjacency == [[], [2], [1, 3], [2]]
