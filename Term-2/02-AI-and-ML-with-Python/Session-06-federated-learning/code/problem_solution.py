"""Session 06 - Real-life problem: federated loan-default model across five bank branches."""
# notebook: run-in-code-dir
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from fl import accuracy, fedavg, local_train

BRANCHES = {"Karachi": 1200, "Lahore": 900, "Islamabad": 500, "Quetta": 150, "Peshawar": 250}


def make_branch(n, shift, rng):
    income = rng.normal(80 + shift * 20, 25, n)          # thousand PKR / month
    debt_ratio = rng.beta(2, 5 - shift, n)
    late_payments = rng.poisson(1 + shift, n)
    age = rng.integers(21, 65, n)
    X = np.column_stack([income, debt_ratio, late_payments, age])
    logit = -0.03 * (income - 80) + 4 * (debt_ratio - 0.3) + 0.5 * (late_payments - 1) - 0.02 * (age - 40)
    y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(float)
    return X, y


def build(seed=4):
    rng = np.random.default_rng(seed)
    parts = [make_branch(n, s, rng) for n, s in zip(BRANCHES.values(), [0.0, 0.5, 1.0, 2.0, 1.5])]
    test = make_branch(1500, 1.0, rng)
    scaler = StandardScaler().fit(np.vstack([p[0] for p in parts]))   # in practice: agreed public stats
    clients = [(scaler.transform(X), y) for X, y in parts]
    return clients, (scaler.transform(test[0]), test[1])


if __name__ == "__main__":
    clients, (X_te, y_te) = build()
    d = clients[0][0].shape[1] + 1
    X_all = np.vstack([c[0] for c in clients]); y_all = np.concatenate([c[1] for c in clients])
    central_w = local_train(np.zeros(d), X_all, y_all, 30, 0.2)
    fed_w, _ = fedavg(clients, rounds=25, epochs=3, lr=0.2)
    dp_w, _ = fedavg(clients, rounds=25, epochs=3, lr=0.2, dp_clip=1.0, dp_sigma=0.3, seed=1)
    local = {name: accuracy(local_train(np.zeros(d), Xk, yk, 75, 0.2), X_te, y_te)
             for name, (Xk, yk) in zip(BRANCHES, clients)}
    results = {"central": accuracy(central_w, X_te, y_te), "fedavg": accuracy(fed_w, X_te, y_te),
               "fedavg+DP": accuracy(dp_w, X_te, y_te), "local_mean": float(np.mean(list(local.values())))}
    print({k: round(v, 3) for k, v in results.items()})
    print("local by branch:", {k: round(v, 3) for k, v in local.items()})
    mb = 25 * len(clients) * fed_w.size * 8 / 1e6
    print(f"uploaded: {mb:.4f} MB (tiny model: {fed_w.size} weights)")
    assert results["fedavg"] >= results["local_mean"] - 0.01
    assert abs(results["fedavg"] - results["central"]) < 0.05
    print("OK")
