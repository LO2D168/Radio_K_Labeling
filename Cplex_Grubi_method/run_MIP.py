import time
from collections import deque
import pandas as pd

import list_instance
import read_file
import cal_bound
from check_labeling import check_labeling
from cplex_model import solve_k_label_cplex
from gurobi_model import solve_k_label_gurobi
from cplex_model_binary import solve_k_label_cplex_binary_version

def adj_to_dist(n, adj):
    dist = [[-1] * (n + 1) for _ in range(n + 1)]
    for s in range(1, n + 1):
        dist[s][s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if dist[s][v] == -1:
                    dist[s][v] = dist[s][u] + 1
                    q.append(v)
    return dist


def run_all(solver_name, time_limit=1200):
    results = []

    for idx, filename in enumerate(list_instance.list_data):
        start = time.time()

        n, q, adj = read_file.read_mtx_to_adj(filename)
        dist = adj_to_dist(n, adj)
        k = cal_bound.get_k_from_filename(dist)
        ub = cal_bound.get_upper_bound(filename, n, k, dist)
        status = "TIMEOUT"

        print(f"Solving {filename} | n={n} | k={k} | ub={ub}")

        if ub != 0:
            if solver_name == "cplex":
                res = solve_k_label_cplex(n, dist, k, ub, time_limit=time_limit)
            elif solver_name == "gurobi":
                res = solve_k_label_gurobi(n, dist, k, ub, time_limit=time_limit)
            elif solver_name == "cplex_binary":
                res = solve_k_label_cplex_binary_version(n, dist, k, ub, time_limit=time_limit)
            else:
                raise ValueError("solver_name must be 'cplex' or 'gurobi'")

            status = res["status"]
            ok, max_label = check_labeling(n, k, dist, res["labels"])
            max_label = int(max_label) - 1
        else:
            ok, max_label = True, 0
            status = "OPTIMIZE"

        results.append({
            "Id": idx,
            "Problem": filename,
            "Num_ver": n,
            "K_val": k,
            "UB": ub,
            "Result": max_label if ok else None,
            "Status": status,
            "Runtime": round(time.time() - start, 4),
        })

        pd.DataFrame(results).to_csv(f"result_{solver_name}.csv", index=False)

    return results


if __name__ == "__main__":
    run_all(solver_name="gurobi", time_limit=1200)