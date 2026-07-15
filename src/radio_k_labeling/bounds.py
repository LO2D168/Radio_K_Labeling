"""Bounds used by the original radio k-labeling search."""


def graph_diameter(distances: list[list[int]]) -> int:
    """Return the maximum finite entry in a distance matrix."""
    finite = [distance for row in distances for distance in row if distance >= 0]
    return max(finite, default=0)


def get_k(distances: list[list[int]]) -> int:
    """Return the radio parameter used by this project: the graph diameter."""
    return graph_diameter(distances)


def upper_bound(vertex_count: int, k: int, distances: list[list[int]]) -> int:
    """Return the historical upper bound ``n * (k + 1) - diameter``."""
    return vertex_count * (k + 1) - graph_diameter(distances)


def get_k_from_filename(distances):
    """Legacy name retained for callers that now pass a distance matrix."""
    return get_k(distances)


def get_upper_bound(filename, n, k, dist):
    """Legacy wrapper; ``filename`` is intentionally ignored."""
    return upper_bound(n, k, dist)
