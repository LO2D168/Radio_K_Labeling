def check_labeling(n, k, dist, labels):
    if labels is None:
        return False, None

    for i in range(1, n + 1):
        if i not in labels:
            print(f"Missing label at vertex {i}")
            return False, None

    for u in range(1, n):
        for v in range(u + 1, n + 1):
            req = k - dist[u][v] + 1
            if req > 0 and abs(labels[u] - labels[v]) < req:
                print(f"Vi phạm: ({u},{v}) with "
                      f"|{labels[u]}-{labels[v]}| < {req}")
                return False, None

    return True, max(labels.values())