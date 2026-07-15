"""Timeout adapter for PySAT solvers.

The child process boundary is intentional: a timed-out native solver cannot be
reliably stopped from a Python thread.
"""

from multiprocessing import get_all_start_methods, get_context
from traceback import format_exc


def _solve_child(connection, solver, assumptions):
    try:
        solved = solver.solve(assumptions=assumptions) if assumptions else solver.solve()
        model = solver.get_model() if solved else None
        connection.send(("On_Time", solved, model))
    except Exception:
        connection.send(("Error", False, format_exc()))
    finally:
        connection.close()


def solve_with_timeout(solver, timeout: float, assumptions=None):
    """Return the legacy ``(status, satisfiable, model)`` tuple."""
    context_name = "fork" if "fork" in get_all_start_methods() else "spawn"
    context = get_context(context_name)
    parent, child = context.Pipe(False)
    process = context.Process(target=_solve_child, args=(child, solver, assumptions))
    process.start()
    child.close()
    if parent.poll(timeout):
        result = parent.recv()
    else:
        process.terminate()
        result = ("Time_Out", None, None)
    process.join(1.0)
    parent.close()
    return result
