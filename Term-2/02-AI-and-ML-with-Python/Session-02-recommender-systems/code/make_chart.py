"""Session 02 - README image: sparse ratings matrix and the MF reconstruction."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from recsys import factorise, make_ratings

R_true, R, mask = make_ratings()
P, Q, B = factorise(R, mask)
fig, axes = plt.subplots(1, 3, figsize=(14, 4), layout="constrained")
for ax, M, t in zip(axes, [np.where(mask, R, np.nan), B + P @ Q.T, R_true],
                    ["Observed ratings (30 % filled)", "Matrix factorisation estimate", "True (hidden) ratings"]):
    im = ax.imshow(M, cmap="viridis", vmin=1, vmax=5, aspect="auto"); ax.set(title=t, xlabel="drama", ylabel="user")
fig.colorbar(im, ax=axes, shrink=0.8)
fig.savefig("../images/recsys.png", dpi=110); plt.close(fig)
print("saved recsys.png")
