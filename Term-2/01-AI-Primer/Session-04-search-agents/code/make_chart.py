"""Session 04 - README image: nodes expanded by BFS, UCS, A* on 8-puzzle instances."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from problems import EightPuzzle
from search import astar, breadth_first, manhattan, misplaced

rng = np.random.default_rng(4)
goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
p = EightPuzzle(goal); s = goal
starts = []
REV = {"U": "D", "D": "U", "L": "R", "R": "L"}
for depth in (8, 14, 20):
    s, last = goal, None
    for _ in range(depth):
        a = rng.choice([m for m in p.actions(s) if m != REV.get(last)])
        s, last = p.result(s, a), a
    starts.append(s)
labels, data = ["BFS", "A* misplaced", "A* Manhattan"], []
for st in starts:
    row = []
    for algo in (lambda q, d: breadth_first(q, stats=d), lambda q, d: astar(q, misplaced, d), lambda q, d: astar(q, manhattan, d)):
        d = {}; algo(EightPuzzle(st), d); row.append(d["expanded"])
    data.append(row)
data = np.array(data)
fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
w = 0.25
for i, lab in enumerate(labels):
    ax.bar(np.arange(3) + i * w, data[:, i], w, label=lab)
ax.set_xticks(np.arange(3) + w, ["start A", "start B", "start C"]); ax.set_yscale("log")
ax.set(title="8-puzzle: nodes expanded (log scale)", ylabel="nodes expanded"); ax.legend()
fig.savefig("../images/search.png", dpi=110); plt.close(fig)
print("saved search.png", data.tolist())
