from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType

def label_condition(n, m, dist, k):
    def getVal(i, j):   # id biến: 1..n^2
        return (i - 1) * m + j

    solver = Cadical195()

    num_var = m * m
    num_clause = 0

    top_id = num_var

    for i in range(1, n + 1):
        lits = [getVal(i, j) for j in range(1, m + 1)]

        cnf = CardEnc.equals(
            lits=lits,
            bound=1,
            top_id=top_id,
            encoding=EncType.seqcounter
        )

        for clause in cnf.clauses:
            solver.add_clause(clause)

        num_clause += len(cnf.clauses)
        top_id = max(top_id, cnf.nv)

    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            val = k - dist[u][v] + 1

            if val <= 0:
                continue

            for a in range(1, m + 1):
                bad_labels = []

                for b in range(1, m + 1):
                    if abs(a - b) < val:
                        bad_labels.append(getVal(v, b))

                if len(bad_labels) == 0:
                    continue

                lits = [getVal(u, a)] + bad_labels

                cnf = CardEnc.atmost(
                    lits=lits,
                    bound=1,
                    top_id=top_id,
                    encoding=EncType.seqcounter                )

                for clause in cnf.clauses:
                    solver.add_clause(clause)

                num_clause += len(cnf.clauses)
                top_id = max(top_id, cnf.nv)

    num_var = top_id

    return num_clause, num_var, solver

def remove_label(n, m, val, solver):
    def getVal(i, j):
        return (i - 1) * m + j

    num_clause = 0
    for i in range(1, n + 1):
        solver.add_clause([-getVal(i, val)])
        num_clause += 1

    return num_clause