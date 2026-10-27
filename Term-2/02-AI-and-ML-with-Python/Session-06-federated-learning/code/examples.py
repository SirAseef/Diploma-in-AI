"""Session 06 - Federated Learning: worked examples."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - split one dataset across clients

# %%
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from fl import accuracy, fedavg, local_train, secure_sum, split_clients

X, y = make_classification(3000, n_features=10, n_informative=6, random_state=6)
X = StandardScaler().fit_transform(X)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, random_state=0)
clients = split_clients(X_tr, y_tr, n_clients=5, iid=False)
for k, (Xk, yk) in enumerate(clients):
    print(f"client {k}: n={len(yk)}, positive share={yk.mean():.2f}, mean x0={Xk[:, 0].mean():+.2f}")

# %% [markdown]
# ## Example 2 - a NumPy logistic-regression client

# %%
w0 = np.zeros(X.shape[1] + 1)
w_local = local_train(w0, *clients[0], epochs=5, lr=0.1)
print("client 0 alone, test accuracy:", round(accuracy(w_local, X_te, y_te), 3))

# %% [markdown]
# ## Example 3 - FedAvg

# %%
fed_w, history = fedavg(clients, rounds=20, epochs=5, X_test=X_te, y_test=y_te)
print("accuracy by round:", np.round(history[::4], 3), "final:", round(history[-1], 3))

# %% [markdown]
# ## Example 4 - compare with centralised and local-only

# %%
central_w = local_train(w0, X_tr, y_tr, epochs=30)
print("centralised:", round(accuracy(central_w, X_te, y_te), 3))
print("federated  :", round(accuracy(fed_w, X_te, y_te), 3))
print("local-only :", [round(accuracy(local_train(w0, Xk, yk, 30), X_te, y_te), 3) for Xk, yk in clients])

# %% [markdown]
# ## Example 5 - secure aggregation with cancelling masks

# %%
w_a, w_b, w_c = np.array([1.0, 2.0]), np.array([0.5, -1.0]), np.array([2.0, 0.0])
masked, total = secure_sum([w_a, w_b, w_c], seed=1)
print("what the server sees from client A:", masked[0].round(1))
print("sum of masked vectors:", total.round(6), "| true sum:", w_a + w_b + w_c)

# %% [markdown]
# ## Example 6 - differential privacy: clip + noise

# %%
for sigma in (0.0, 0.5, 1.5):
    _, h = fedavg(clients, rounds=20, X_test=X_te, y_test=y_te, dp_clip=1.0, dp_sigma=sigma, seed=2)
    print(f"sigma={sigma}: final accuracy {h[-1]:.3f}")
