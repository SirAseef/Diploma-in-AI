"""Session 06 - Practice exercise solutions."""
# notebook: run-in-code-dir
import itertools
import time
from logic import backward_chain, entails, forward_chain, implies, is_valid


def ex1():
    rows = [(P, Q, implies(P and Q, P)) for P, Q in itertools.product([True, False], repeat=2)]
    return rows, is_valid(lambda m: implies(m["P"] and m["Q"], m["P"]), ["P", "Q"])


def ex2():
    return entails(lambda m: implies(m["P"], m["Q"]) and not m["Q"], lambda m: not m["P"], ["P", "Q"])


def ex3():
    big = [(["A"], "B"), (["B"], "C")] + [(["A"], f"X{i}") for i in range(30)]
    _, fired = forward_chain(big, {"A"})
    _, steps = backward_chain(big, {"A"}, "C")
    return fired, steps


def ex4():
    times = {}
    for n in (10, 14, 18):
        syms = [f"S{i}" for i in range(n)]
        t0 = time.perf_counter(); entails(lambda m: True, lambda m: True, syms)
        times[n] = time.perf_counter() - t0
    return times, times[18] * 2 ** 12


if __name__ == "__main__":
    rows, valid = ex1(); print("ex1", rows, "valid:", valid); assert valid
    print("ex2 modus tollens holds:", ex2()); assert ex2()
    f, s = ex3(); print("ex3 forward fired:", f, "backward steps:", s); assert f > s
    t, est = ex4(); print("ex4", {k: round(v, 4) for k, v in t.items()}, "est 30 symbols ~", round(est), "s")
    assert t[18] > t[10]
    print("all exercises OK")
