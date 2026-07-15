"""Independent validation of candidate radio labelings."""


def validate_labeling(
    labels: dict[int, int] | list[int],
    k: int,
    distances: list[list[int]],
) -> tuple[bool, int | None]:
    """Validate ``|c(u)-c(v)| >= k-dist(u,v)+1`` for every vertex pair.

    The return value is ``(valid, maximum_label)``. A list follows the same
    1-based convention as the legacy SAT model and therefore must have an
    unused element at index zero.
    """
    if isinstance(labels, list):
        if len(labels) != len(distances):
            return False, None
        values = {vertex: labels[vertex] for vertex in range(1, len(distances))}
    else:
        values = labels
        if any(vertex not in values for vertex in range(1, len(distances))):
            return False, None

    for u in range(1, len(distances)):
        for v in range(u + 1, len(distances)):
            required = k - distances[u][v] + 1
            if required > 0 and abs(values[u] - values[v]) < required:
                return False, None
    return True, max(values.values(), default=None)


def check_labeling(n, k, dist, labels):
    """Legacy-compatible wrapper returning ``(valid, maximum_label)``."""
    return validate_labeling(labels, k, dist)
