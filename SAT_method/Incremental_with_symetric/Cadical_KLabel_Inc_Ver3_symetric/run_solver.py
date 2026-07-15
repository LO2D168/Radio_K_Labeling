import multiprocessing as mp
import traceback

def _solve_worker(solver, assumptions, conn):
    try:
        if assumptions is None:
            sat = solver.solve()
        else:
            sat = solver.solve(assumptions=assumptions)
        model = solver.get_model() if sat else None
        conn.send(("On_Time", sat, model))
    except Exception:
        conn.send(("Error", False, traceback.format_exc()))
    finally:
        conn.close()

def solve_with_timeout(solver, timeout: float, assumptions=None):
    if timeout is None or timeout <= 0:
        return "Time_Out", None, None

    ctx = mp.get_context("fork")
    parent_conn, child_conn = ctx.Pipe(duplex=False)
    p = ctx.Process(target=_solve_worker, args=(solver, assumptions, child_conn), daemon=True)
    p.start()
    child_conn.close()

    if parent_conn.poll(timeout):
        status, a, b = parent_conn.recv()
        p.join(timeout=0.2)
        if status == "On_Time":
            return status, a, b
        return "Error", None, b

    p.terminate()
    p.join(timeout=1.0)
    return "Time_Out", None, None
