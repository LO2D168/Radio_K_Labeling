from docplex.mp.model import Model

def solve_k_label_cplex_binary_version(n, dist, k, ub, time_limit=1200):
    mdl = Model(name="k_label_cplex")
    mdl.parameters.timelimit = time_limit

    x = {(v, l): mdl.binary_var(name=f"x_{v}_{l}") for v in range(1, n + 1) for l in range(1, ub + 1)}
    z = mdl.integer_var(lb=0, name="z")

    for v in range(1, n + 1):
        mdl.add_constraint(mdl.sum(x[v, l] for l in range(1, ub + 1)) == 1)

    for l in range(1, ub + 1):
        mdl.add_constraint(mdl.sum(x[v, l] for v in range(1, n + 1)) <= 1)

    label_val = {v: mdl.sum(l * x[v, l] for l in range(1, ub + 1)) for v in range(1, n + 1)}

    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            delta_uv = k - dist[u][v] + 1
            if delta_uv > 0:
                for l1 in range(1, ub + 1):
                    for l2 in range(1, ub + 1):
                        if abs(l1 - l2) < delta_uv:
                            mdl.add_constraint(x[u, l1] + x[v, l2] <= 1)

    for v in range(1, n + 1):
        mdl.add_constraint(z >= label_val[v])

    mdl.minimize(z)

    sol = mdl.solve()

    if sol is None:
        return {
            "status": str(mdl.solve_details.status),
            "objective": None,
            "labels": None,
        }

    labels = {i: int(round(sol[label_val[i]])) for i in range(1, n + 1)}

    return {
        "status": str(mdl.solve_details.status),
        "objective": int(round(sol[z])),
        "labels": labels,
    }