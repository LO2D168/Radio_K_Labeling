"""Matrix Market graph input."""

from pathlib import Path

import networkx as nx
import numpy as np
from scipy.io import mmread


def read_mtx_to_adj(path: str | Path) -> tuple[int, int, list[list[int]]]:
    matrix_path = Path(path)
    if not matrix_path.is_file():
        raise FileNotFoundError(matrix_path)
    matrix = mmread(matrix_path)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError(f"expected a square adjacency matrix: {matrix_path}")
    if hasattr(matrix, "tocoo"):
        matrix = matrix.tocoo()
        rows, columns = matrix.row, matrix.col
    else:
        rows, columns = np.nonzero(np.asarray(matrix))
    graph = nx.Graph()
    graph.add_nodes_from(range(matrix.shape[0]))
    graph.add_edges_from((int(row), int(column)) for row, column in zip(rows, columns))
    graph.remove_edges_from(nx.selfloop_edges(graph))
    graph = nx.convert_node_labels_to_integers(graph)
    adjacency = [[] for _ in range(graph.number_of_nodes() + 1)]
    for u, v in graph.edges:
        adjacency[u + 1].append(v + 1)
        adjacency[v + 1].append(u + 1)
    return graph.number_of_nodes(), graph.number_of_edges(), adjacency
