from pysat.solvers import Cadical195

def label_condition(n, m, dist, k):
    def getG(i, j):
        return (i - 1) * m + j

    solver = Cadical195()

    num_var = 2 * n * m
    num_clause = 0

    for i in range(1, n + 1):
        for j in range(1, m):
            solver.add_clause([-getG(i, j + 1), getG(i, j)])
            num_clause += 1

    for i in range(1, n + 1):
        solver.add_clause([getG(i, 1)])
        num_clause += 1

    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            val = k - dist[u][v] + 1
            if val <= 0: continue
            for _val in range(1, m):
                if _val + val <= m and _val > val - 1:
                    solver.add_clause([getG(u, _val + 1), -getG(u, _val), -getG(v, _val - val + 1), getG(v, _val + val)])
                    num_clause += 1
                else:
                    if _val > val - 1:
                        solver.add_clause([getG(u, _val + 1), -getG(u, _val), -getG(v, _val - val + 1)])
                        num_clause += 1
                    if _val + val <= m:
                        solver.add_clause([getG(u, _val + 1), -getG(u, _val), getG(v, _val + val)])
                        num_clause += 1

            if m + val <= m and m > val - 1:
                solver.add_clause([-getG(u, m), -getG(v, m - val + 1), getG(v, m + val)])
                num_clause += 1
            else:
                if m > val - 1:
                    solver.add_clause([-getG(u, m), -getG(v, m - val + 1)])
                    num_clause += 1
                if m + val <= m:
                    solver.add_clause([-getG(u, m), getG(v, m + val)])
                    num_clause += 1

    return num_clause, num_var, solver
