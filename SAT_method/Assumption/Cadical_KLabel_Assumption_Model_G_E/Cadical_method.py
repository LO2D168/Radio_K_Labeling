import time
from collections import deque

import list_instance, check_model, read_file, Constraint_model, cal_bound, run_solver
import pandas

results = []
for id in range(0, len(list_instance.list_data)):

    start_time = time.time()
    filename = list_instance.list_data[id]
    n, q, adj = read_file.read_mtx_to_adj(filename)

    time_limit = 1200
    result = 0
    status = "TIME_OUT"
    total_clause = 0
    total_var = 0

    def adj_to_dist():
        dist = [[-1] * (n + 3) for _ in range(n + 3)]
        for s in range(1, n + 1):
            d = dist[s]
            d[s] = 0
            q = deque([s])
            while q:
                u = q.popleft()
                for v in adj[u]:
                    if d[v] == -1:
                        d[v] = d[u] + 1
                        q.append(v)
        return dist

    dist = adj_to_dist()
    k = cal_bound.get_k_from_filename(dist)
    ub = cal_bound.get_upper_bound(filename, n, k, dist)
    lb = 1
    print("Đang giải instace: ", filename, id, ub, n, k, "bound: ", lb, ub)

    num_clause, num_var, solver = Constraint_model.label_condition(n, ub, dist, k)
    total_var += num_var
    total_clause += num_clause

    removed_labels = ub

    def getVal(i, j):
        return (i - 1) * ub + j

    def getMask(i, j):
        return n * ub + (i - 1) * ub + j

    def build_assumptions():
        assumps = []
        for i in range(1, n + 1):
            assumps.append(-getVal(i, removed_labels))
            assumps.append(-getMask(i, removed_labels))
        return assumps

    val = ub
    while val >= lb:
        if time.time() - start_time > time_limit:
            result = val
            status = "TIME_OUT"
            break

        remain = time_limit - (time.time() - start_time)
        print("Instance: ", filename, "| value check: ", val - 1, "| remain time: ", remain)

        assumptions = build_assumptions()
        status_solver, sat, model = run_solver.solve_with_timeout(solver, remain, assumptions=assumptions)

        bestBound = val

        if status_solver == "On_Time":
            if sat:
                biggest_val, check = check_model.check(n, k, dist, ub, model)
                bestBound = biggest_val
                if check:
                    result = bestBound - 1
                    print("value is: ", result)
                    status = "OPTIMIZE"
                else:
                    break
            else:
                break
        else:
            result = val
            status = "TIME_OUT"
            break

        removed_labels = bestBound
        val = bestBound - 1

    results.append({
        "Id": id,
        "Problem": filename,
        "Num_ver": n,
        "K_val": k,
        "Num_clause": total_clause,
        "Num_var": total_var,
        "UB: ": ub,
        "Result": result,
        "Status": status,
        "Runtime": round(time.time() - start_time, 4)
    })
    df = pandas.DataFrame(results)
    df.to_csv("Cadical_Assumption_ver5.csv", index=False)
