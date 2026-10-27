"""Session 07 - Quantum Computing and ML Integration: worked examples."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - one qubit, superposition and measurement

# %%
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from qsim import H, apply, cnot, feature_map, measure, probabilities, quantum_kernel, train_vqc, vqc_prob, zero_state

state = apply(H, zero_state(1), target=0, n=1)
print("amplitudes:", state.round(3), "probabilities:", probabilities(state).round(3))
print("1000 shots:", measure(state, shots=1000, seed=0))

# %% [markdown]
# ## Example 2 - entanglement: a Bell state

# %%
s = apply(H, zero_state(2), 0, 2)
s = cnot(s, control=0, target=1, n=2)
print("Bell state amplitudes:", s.round(3))
print("1000 shots:", measure(s, 1000, seed=1))

# %% [markdown]
# ## Example 3 - encode data with a feature map

# %%
print("feature map of [0.3, 1.2]:", np.round(probabilities(feature_map([0.3, 1.2])), 3))

# %% [markdown]
# ## Example 4 - a quantum kernel inside SVC

# %%
rng = np.random.default_rng(7)
X = rng.uniform(-1, 1, (100, 2)); y = (X[:, 0] * X[:, 1] > 0).astype(int)   # XOR-like quadrants
Xs = MinMaxScaler((0, np.pi)).fit_transform(X)
X_tr, X_te, y_tr, y_te = train_test_split(Xs, y, test_size=0.3, random_state=0, stratify=y)
svc = SVC(kernel="precomputed").fit(quantum_kernel(X_tr, X_tr), y_tr)
print("quantum-kernel SVM accuracy:", round(svc.score(quantum_kernel(X_te, X_tr), y_te), 3))

# %% [markdown]
# ## Example 5 - a variational classifier with the parameter-shift rule

# %%
Xv = rng.uniform(0, np.pi, (60, 2)); yv = (Xv[:, 0] > Xv[:, 1]).astype(float)
theta, losses = train_vqc(Xv[:40], yv[:40], epochs=40)
pred = np.array([vqc_prob(x, theta) > 0.5 for x in Xv[40:]])
print("loss first/last:", round(losses[0], 3), round(losses[-1], 3), "| test accuracy:", (pred == yv[40:]).mean())

# %% [markdown]
# ## Example 6 - compare with a classical model

# %%
print("classical RBF SVM on the Example 4 data:", round(SVC().fit(X_tr, y_tr).score(X_te, y_te), 3))
