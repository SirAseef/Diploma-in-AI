"""Session 03 - Practice exercise solutions."""
# notebook: run-in-code-dir
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import CategoricalNB
from bn import BayesNet, example_net, rejection_sample

net = example_net()


def ex1():
    by_hand = 0.95 * 0.02 / (0.95 * 0.02 + 0.10 * 0.98)
    test = BayesNet(); test.add("Disease", [], {(): 0.02})
    test.add("Positive", ["Disease"], {(True,): 0.95, (False,): 0.10})
    return by_hand, test.query("Disease", {"Positive": True})[True]


def ex2():
    return net.query("UPSBeeps", {"Summer": True})[True]


def ex3():
    ev = {"GeneratorOn": True}; exact = net.query("LoadShedding", ev)[True]
    return {n: abs(rejection_sample(net, "LoadShedding", ev, n, seed=3)[True] - exact) for n in (500, 5000, 50000)}


def ex4():
    df = net.sample_df(4000, seed=2).astype(int)
    X, y = df.drop(columns="LoadShedding"), df["LoadShedding"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, random_state=0)
    return CategoricalNB().fit(X_tr, y_tr).score(X_te, y_te)


if __name__ == "__main__":
    h, c = ex1(); print("ex1 by hand", round(h, 4), "network", round(c, 4)); assert abs(h - c) < 1e-9
    p = ex2(); print("ex2 P(UPSBeeps | Summer)", round(p, 3)); assert abs(p - (0.7 * 0.8 + 0.3 * 0.05)) < 1e-9
    e = ex3(); print("ex3 errors", {k: round(v, 4) for k, v in e.items()}); assert e[50000] < 0.02
    a = ex4(); print("ex4 CategoricalNB accuracy", round(a, 3)); assert a > 0.75
    print("all exercises OK")
