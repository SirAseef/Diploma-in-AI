"""Session 07 - README image: quantum kernel matrix and VQC training loss."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from qsim import quantum_kernel, train_vqc

rng = np.random.default_rng(0)
Xa = rng.uniform(0, np.pi, (40, 2)); order = np.argsort(Xa[:, 0] + Xa[:, 1]); Xa = Xa[order]
K = quantum_kernel(Xa, Xa)
Xv = rng.uniform(0, np.pi, (40, 2)); yv = (Xv[:, 0] > Xv[:, 1]).astype(float)
_, losses = train_vqc(Xv, yv, epochs=40)
fig, axes = plt.subplots(1, 2, figsize=(11, 4), layout="constrained")
im = axes[0].imshow(K, cmap="magma"); axes[0].set_title("Quantum kernel matrix (40 points)"); fig.colorbar(im, ax=axes[0])
axes[1].plot(losses, marker="."); axes[1].set(title="Variational classifier: training loss", xlabel="epoch", ylabel="MSE")
fig.savefig("../images/quantum.png", dpi=110); plt.close(fig)
print("saved quantum.png")
