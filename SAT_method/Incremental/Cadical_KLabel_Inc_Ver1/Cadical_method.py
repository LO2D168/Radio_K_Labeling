import time
from collections import deque

import list_instance, check_model, read_file, Constraint_model, cal_bound, run_solver
import pandas

results = []
for id in range(89, len(list_instance.list_data)):

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

    val = ub

    while val >= lb:
        if time.time() - start_time > time_limit:
            result = val
            status = "TIME_OUT"
            break

        print("Instance: ", filename, "| value check: ", val - 1, "| remain time: ", time_limit - (time.time() - start_time))
        status_solver, sat, model = run_solver.solve_with_timeout(solver, time_limit - (time.time() - start_time))
        bestBound = val

        if status_solver == "On_Time":
            if sat:
                biggest_val, check = check_model.check(n, k, dist, ub, model)
                bestBound = biggest_val
                if check:
                    print("value is: ", bestBound - 1)
                    result = bestBound - 1
                    status = "OPTIMIZE"
                else:
                    break
            else:
                break
        else:
            result = val
            status = "TIME_OUT"
            break

        num_inc_clause = Constraint_model.remove_label(n, ub, bestBound, solver)
        total_clause += num_inc_clause
        val = bestBound- 1

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
    df.to_csv("result_del_G_E_2.csv", index=False)