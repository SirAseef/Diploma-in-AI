"""Session 02 - README image: activation functions and XOR decision boundary."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neural_network import MLPClassifier

z = np.linspace(-5, 5, 200)
fig, axes = plt.subplots(1, 2, figsize=(11, 4), layout="constrained")
axes[0].plot(z, 1 / (1 + np.exp(-z)), label="sigmoid"); axes[0].plot(z, np.tanh(z), label="tanh")
axes[0].plot(z, np.maximum(0, z) / 5, label="ReLU (scaled /5)"); axes[0].legend(); axes[0].set_title("Activation functions")
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]] * 25, dtype=float)
y = np.array([0, 1, 1, 0] * 25)
X += np.random.default_rng(0).normal(0, 0.08, X.shape)
m = MLPClassifier((8,), activation="tanh", solver="lbfgs", max_iter=2000, random_state=1).fit(X, y)
gx, gy = np.meshgrid(np.linspace(-0.5, 1.5, 200), np.linspace(-0.5, 1.5, 200))
p = m.predict(np.c_[gx.ravel(), gy.ravel()]).reshape(gx.shape)
axes[1].contourf(gx, gy, p, alpha=0.3, cmap="coolwarm"); axes[1].scatter(X[:, 0], X[:, 1], c=y, cmap="coolwarm", s=12)
axes[1].set_title("A small network separates XOR")
fig.savefig("../images/deep_learning.png", dpi=110); plt.close(fig)
print("saved deep_learning.png")
