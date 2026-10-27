"""Session 02 - Practice exercise solutions."""
import numpy as np


def diag_and_block():
    a = np.arange(1, 17).reshape(4, 4)
    return np.diag(a), a[2:, 2:]


def hot_fahrenheit(celsius, limit=95):
    f = np.asarray(celsius) * 9 / 5 + 32
    return f[f > limit]


def standardise(x):
    return (x - x.mean(axis=0)) / x.std(axis=0)


def coin_probability(n=1000, seed=0):
    return np.random.default_rng(seed).integers(0, 2, n).mean()


if __name__ == "__main__":
    d, b = diag_and_block()
    assert list(d) == [1, 6, 11, 16] and b.tolist() == [[11, 12], [15, 16]]
    assert list(hot_fahrenheit([28, 33, 36, 40, 31])) == [96.8, 104.0]
    z = standardise(np.array([[1.0, 10], [2, 20], [3, 30]]))
    assert np.allclose(z.mean(axis=0), 0) and np.allclose(z.std(axis=0), 1)
    p = coin_probability()
    assert 0.45 < p < 0.55
    print("All exercise checks passed; p(heads) =", p)
