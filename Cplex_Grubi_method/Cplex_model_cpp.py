from docplex.cp.model import CpoModel
from docplex.cp.modeler import abs_of


def solve_k_label_cp(n, dist, k, ub, time_limit=1200):
    mdl = CpoModel(name="k_label_cp")

    x = {i: mdl.integer_var(min=1, max=ub, name=f"x_{i}") for i in range(1, n + 1)}
    z = mdl.integer_var(min=1, max=ub, name="z")

    for i in range(1, n + 1):
        mdl.add(x[i] <= z)

    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            req = k - dist[u][v] + 1
            if req <= 0:
                continue

            mdl.add(abs_of(x[u] - x[v]) >= req)

    mdl.add(mdl.minimize(z))

    sol = mdl.solve(
        TimeLimit=time_limit,
        LogVerbosity='Quiet',
        WarningLevel=0,
        Workers=1
    )

    if sol is None:
        return {
            "status": "No solution",
            "objective": None,
            "labels": None,
        }

    labels = {i: sol[x[i]] for i in range(1, n + 1)}
    return {
        "status": sol.get_solve_status(),
        "objective": sol[z],
        "labels": labels,
    }