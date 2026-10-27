"""Session 02 - Deep Learning: worked examples."""

# %% [markdown]
# ## Example 1 - one artificial neuron

# %%
import warnings
import numpy as np
from sklearn.datasets import load_digits
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
warnings.filterwarnings("ignore", category=ConvergenceWarning)

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def neuron(x, w, b):
    return sigmoid(np.dot(w, x) + b)

print("neuron output:", round(float(neuron(np.array([1, 0]), np.array([2.0, -1.0]), -0.5)), 3))

# %% [markdown]
# ## Example 2 - a single neuron learns AND but not XOR

# %%
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y_and = np.array([0, 0, 0, 1]); y_xor = np.array([0, 1, 1, 0])
for name, yy in {"AND": y_and, "XOR": y_xor}.items():
    p = Perceptron(max_iter=100, random_state=0).fit(X, yy)
    print(name, "accuracy:", p.score(X, yy))

# %% [markdown]
# ## Example 3 - a two-layer network from scratch solves XOR

# %%
rng = np.random.default_rng(0)
yx = y_xor.reshape(-1, 1).astype(float)
W1, b1 = rng.normal(size=(2, 4)), np.zeros(4)
W2, b2 = rng.normal(size=(4, 1)), np.zeros(1)
lr = 0.5
for epoch in range(5000):
    h = np.tanh(X @ W1 + b1)
    out = sigmoid(h @ W2 + b2)
    d_out = (out - yx) / len(X)
    d_h = (d_out @ W2.T) * (1 - h ** 2)
    W2 -= lr * h.T @ d_out; b2 -= lr * d_out.sum(0)
    W1 -= lr * X.T @ d_h; b1 -= lr * d_h.sum(0)
    if epoch % 1000 == 0:
        loss = -np.mean(yx * np.log(out) + (1 - yx) * np.log(1 - out))
        print(f"epoch {epoch}: loss {loss:.4f}")
print("predictions:", (out.ravel() > 0.5).astype(int), "target:", y_xor)

# %% [markdown]
# ## Example 4 - gradient descent on one parameter

# %%
w = 0.0
for step in range(50):
    grad = 2 * (w - 3)
    w -= 0.1 * grad
print("w after 50 steps:", round(w, 4), "(minimum is at 3)")

# %% [markdown]
# ## Example 5 - MLPClassifier on handwritten digits

# %%
Xd, yd = load_digits(return_X_y=True)
X_tr, X_te, y_tr, y_te = train_test_split(Xd, yd, test_size=0.25, random_state=0, stratify=yd)
mlp = make_pipeline(StandardScaler(), MLPClassifier(hidden_layer_sizes=(64,), max_iter=300, random_state=0))
mlp.fit(X_tr, y_tr)
print("digits test accuracy:", round(mlp.score(X_te, y_te), 3))

# %% [markdown]
# ## Example 6 - depth vs width

# %%
for layers in [(8,), (64,), (64, 32)]:
    m = make_pipeline(StandardScaler(), MLPClassifier(layers, max_iter=300, random_state=0)).fit(X_tr, y_tr)
    print(layers, round(m.score(X_te, y_te), 3))
