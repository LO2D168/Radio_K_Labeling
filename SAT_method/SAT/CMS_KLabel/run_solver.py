import threading

class Time_Out(Exception):
    pass

def Time_Limit(solver, time_out):
    result = [None]
    exception = [None]

    def sol():
        try:
            sat, model = solver.solve()
            result[0] = ("On_Time", sat, model)
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=sol)
    thread.daemon = True
    thread.start()
    thread.join(timeout=time_out)

    if thread.is_alive():
        print("Time_Out", None)
        return "Time_Out", None, None

    if exception[0]:
        print(f"Eror in solver: {exception[0]}")
        return "Eror", None, None

    if result[0]:
        return result[0]
    else:
        return "Eror", None, None

def solve_with_timeout(solver, timeout):

    return Time_Limit(solver, timeout)


