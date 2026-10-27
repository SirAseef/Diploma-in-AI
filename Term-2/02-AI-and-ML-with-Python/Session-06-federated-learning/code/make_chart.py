"""Session 06 - README image: FedAvg test accuracy per round vs centralised and local-only."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from fl import accuracy, fedavg, local_train, split_clients

X, y = make_classification(3000, n_features=10, n_informative=6, random_state=6)
X = StandardScaler().fit_transform(X)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, random_state=0)
clients = split_clients(X_tr, y_tr, 5, iid=False)
_, hist = fedavg(clients, rounds=25, X_test=X_te, y_test=y_te)
_, hist_dp = fedavg(clients, rounds=25, X_test=X_te, y_test=y_te, dp_clip=1.0, dp_sigma=0.8, seed=1)
central = accuracy(local_train(np.zeros(11), X_tr, y_tr, 30), X_te, y_te)
local = np.mean([accuracy(local_train(np.zeros(11), Xk, yk, 30), X_te, y_te) for Xk, yk in clients])
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
ax.plot(range(1, 26), hist, marker="o", label="FedAvg")
ax.plot(range(1, 26), hist_dp, marker="s", label="FedAvg + DP (sigma 0.8)")
ax.axhline(central, ls="--", color="green", label="centralised")
ax.axhline(local, ls=":", color="red", label="average local-only")
ax.set(xlabel="round", ylabel="test accuracy", title="Federated averaging on non-IID clients"); ax.legend()
fig.savefig("../images/fedavg.png", dpi=110); plt.close(fig)
print("saved fedavg.png")
