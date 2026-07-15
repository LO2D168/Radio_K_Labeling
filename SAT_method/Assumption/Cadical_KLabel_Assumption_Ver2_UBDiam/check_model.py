def check(n, k, dist, val, model):
    pos = [0] * (n + 1)
    limit_var = n * val

    for lit in model:
        if 1 <= lit <= limit_var:
            idx = lit - 1
            u = (idx // val) + 1
            v = (idx % val) + 1
            pos[u] = v

    if 0 in pos[1:]:
        print("Lỗi không gán nhãn")
        return -1, False

    for u in range(1, n):
        pos_u = pos[u]
        for v in range(u + 1, n + 1):
            if abs(pos_u - pos[v]) < k - dist[u][v] + 1:
                print("Không thỏa mãn distance")
                return -1, False

    return max(pos[1:]), True
