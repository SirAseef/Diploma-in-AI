"""Session 03 - Introduction to Problem Solving: worked examples."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Examples 1-2 - the Problem base class and the water-jug problem (see problems.py)

# %%
import math
from problems import EightPuzzle, WaterJug, explore, run_plan

jug = WaterJug()
print("initial:", jug.initial, "actions:", jug.actions(jug.initial))
print("fill A ->", jug.result((0, 0), "fill A"), "| pour A->B from (4,0) ->", jug.result((4, 0), "pour A->B"))

# %% [markdown]
# ## Example 3 - exploring the state space

# %%
reachable = explore(jug)
print(len(reachable), "reachable states:", sorted(reachable))
print("goal states:", sorted(s for s in reachable if jug.is_goal(s)))

# %% [markdown]
# ## Example 4 - the 8-puzzle formulation

# %%
p = EightPuzzle((1, 2, 3, 4, 0, 6, 7, 5, 8))
print("legal moves with blank in centre:", p.actions(p.initial))
print("after D:", p.result(p.initial, "D"))
print("after D then R is goal?", p.is_goal(p.result(p.result(p.initial, "D"), "R")))

# %% [markdown]
# ## Example 5 - checking a plan

# %%
plan = ["fill A", "pour A->B", "empty B", "pour A->B", "fill A", "pour A->B"]
trace = run_plan(jug, plan)
for a, s in zip(["start"] + plan, trace):
    print(f"{a:10s} -> {s}")
print("goal reached:", jug.is_goal(trace[-1]))

# %% [markdown]
# ## Example 6 - how fast state spaces grow

# %%
for n in [3, 4, 5]:
    print(f"{n * n - 1}-puzzle: {math.factorial(n * n) // 2:,} reachable states")
