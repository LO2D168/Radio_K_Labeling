from pysat.solvers import Cadical195

def label_condition(n, m, dist, k):
    def getVal(i, j):   # id biến: 1..n^2
        return (i - 1) * m + j

    def getMask(i, j):
        return n * m + (i - 1) * m + j

    solver = Cadical195()

    num_var = 2 * n * m
    num_clause = 0

    for j in range(1, m):
        for i in range(1, n + 1):
            solver.add_clause([-getMask(i, j), getVal(i, j)])
            solver.add_clause([-getMask(i, j), -getVal(i, j + 1)])
            solver.add_clause([-getVal(i, j), getVal(i, j + 1), getMask(i, j)])
            num_clause += 3

    for i in range(1, n + 1):
        solver.add_clause([-getMask(i, m), getVal(i, m)])
        solver.add_clause([-getVal(i, m), getMask(i, m)])
        num_clause += 2

    for i in range(1, n + 1):
        solver.add_clause([getVal(i, 1)])
        num_clause += 1

    for i in range(1, n + 1):
        for j in range(1, m):
            solver.add_clause([-getVal(i, j + 1), getVal(i, j)])
            num_clause += 1

    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            val = k - dist[u][v] + 1
            if val <= 0: continue
            for _val in range(1, m + 1):
                if _val + val <= m and _val > val - 1:
                    solver.add_clause([-getMask(u, _val), -getVal(v, _val - val + 1), getVal(v, _val + val)])
                    num_clause += 1
                else:
                    if _val > val - 1:
                        solver.add_clause([-getMask(u, _val), -getVal(v, _val - val + 1)])
                        num_clause += 1
                    if _val + val <= m:
                        solver.add_clause([-getMask(u, _val), getVal(v, _val + val)])
                        num_clause += 1

    return num_clause, num_var, solver
