"""Graph operations using the repository's 1-based vertex convention."""

from collections import deque


def adjacency_to_dist(adjacency: list[list[int]]) -> list[list[int]]:
    """Return an ``(n + 1) x (n + 1)`` BFS distance matrix.

    ``adjacency[0]`` is ignored and vertices are expected to be numbered
    from 1 through ``n``. Unreachable pairs retain distance ``-1``.
    """
    n = len(adjacency) - 1
    distances = [[-1] * (n + 1) for _ in range(n + 1)]
    for source in range(1, n + 1):
        distances[source][source] = 0
        queue = deque([source])
        while queue:
            vertex = queue.popleft()
            for neighbor in adjacency[vertex]:
                if not 1 <= neighbor <= n:
                    raise ValueError(f"vertex {neighbor} is outside 1..{n}")
                if distances[source][neighbor] == -1:
                    distances[source][neighbor] = distances[source][vertex] + 1
                    queue.append(neighbor)
    return distances


# Name used by the original drivers.
adj_to_dist = adjacency_to_dist
adjacency_to_distances = adjacency_to_dist
