import gurobipy as gp
from gurobipy import GRB


def solve_k_label_gurobi(n, dist, k, ub, time_limit=1200):
    model = gp.Model("k_label_gurobi_binary")
    model.Params.TimeLimit = time_limit

    x = {
        (v, l): model.addVar(
            vtype=GRB.BINARY,
            name=f"x_{v}_{l}"
        )
        for v in range(1, n + 1)
        for l in range(1, ub + 1)
    }

    z = model.addVar(
        vtype=GRB.INTEGER,
        lb=1,
        ub=ub,
        name="z"
    )

    for v in range(1, n + 1):
        model.addConstr(
            gp.quicksum(x[v, l] for l in range(1, ub + 1)) == 1,
            name=f"one_label_{v}"
        )

    for l in range(1, ub + 1):
        model.addConstr(
            gp.quicksum(x[v, l] for v in range(1, n + 1)) <= 1,
            name=f"unique_label_{l}"
        )

    for v in range(1, n + 1):
        model.addConstr(
            gp.quicksum(l * x[v, l] for l in range(1, ub + 1)) <= z,
            name=f"max_label_{v}"
        )

    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            req = k - dist[u][v] + 1

            if req <= 0:
                continue

            for l1 in range(1, ub + 1):
                for l2 in range(1, ub + 1):
                    if abs(l1 - l2) < req:
                        model.addConstr(
                            x[u, l1] + x[v, l2] <= 1,
                            name=f"dist_{u}_{v}_{l1}_{l2}"
                        )

    model.setObjective(z, GRB.MINIMIZE)
    model.optimize()

    if model.SolCount == 0:
        return {
            "status": model.Status,
            "objective": None,
            "labels": None,
        }

    labels = {}

    for v in range(1, n + 1):
        for l in range(1, ub + 1):
            if x[v, l].X > 0.5:
                labels[v] = l
                break

    obj = int(round(z.X))

    return {
        "status": model.Status,
        "objective": obj,
        "labels": labels,
    }