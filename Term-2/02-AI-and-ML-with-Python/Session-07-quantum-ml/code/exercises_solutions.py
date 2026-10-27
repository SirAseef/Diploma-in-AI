"""Session 07 - Practice exercise solutions."""
# notebook: run-in-code-dir
import numpy as np
from qsim import H, apply, cnot, measure, quantum_kernel, train_vqc, zero_state


def ex1():
    s = apply(H, zero_state(3), 0, 3); s = cnot(s, 0, 1, 3); s = cnot(s, 1, 2, 3)
    return measure(s, 1000, seed=0)


def ex2():
    return apply(H, apply(H, zero_state(1), 0, 1), 0, 1)


def ex3():
    x = np.array([[0.7, 2.1]])
    return quantum_kernel(x, x)[0, 0]


def ex4():
    rng = np.random.default_rng(1)
    X = rng.uniform(0, np.pi, (30, 2)); y = (X[:, 0] > X[:, 1]).astype(float)
    return train_vqc(X, y, epochs=20)[1][-1], train_vqc(X, y, epochs=60)[1][-1]


if __name__ == "__main__":
    c = ex1(); print("ex1 GHZ counts:", c); assert set(c) == {"000", "111"}
    s = ex2(); print("ex2 H.H|0>:", s.round(6)); assert np.allclose(s, [1, 0])
    k = ex3(); print("ex3 k(x, x) =", round(k, 6)); assert abs(k - 1) < 1e-9
    a, b = ex4(); print("ex4 loss after 20 / 60 epochs:", round(a, 4), round(b, 4)); assert b <= a
    print("all exercises OK")
