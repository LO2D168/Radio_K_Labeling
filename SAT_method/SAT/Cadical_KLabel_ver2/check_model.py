def getVal(i, j, n):
    return (i - 1) * n + j

def check(n, k, dist, val, model):
    pos = [-1] * (n + 1)
    for i in range(1, n + 1):
        for j in range(1, val + 1):
            if getVal(i, j, val) in model:
                pos[i] = j

    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            if abs(pos[u] - pos[v]) < k - dist[u][v] + 1:
                print("Không thỏa mãn distance")
                return pos, False

    for i in range(1, n + 1):
        if pos[i] == 0:
            print("Lỗi không gán nhãn")
            return pos, False
    return pos, True