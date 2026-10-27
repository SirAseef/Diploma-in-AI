"""Session 06 - Logical Reasoning and Performance Computation: worked examples."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - truth table for implication

# %%
import itertools
import time
from logic import backward_chain, count_models, entails, forward_chain, implies, is_satisfiable, is_valid

print("P     Q     P->Q")
for P, Q in itertools.product([True, False], repeat=2):
    print(f"{P!s:5} {Q!s:5} {implies(P, Q)}")

# %% [markdown]
# ## Example 2 - entailment by model checking

# %%
def kb(m):
    return implies(m["Holiday"], m["Closed"]) and implies(m["Closed"], m["Canteen"]) and m["Holiday"]

syms = ["Holiday", "Closed", "Canteen"]
print("KB entails Canteen closed:", entails(kb, lambda m: m["Canteen"], syms))
print("KB entails NOT Holiday:", entails(kb, lambda m: not m["Holiday"], syms))

# %% [markdown]
# ## Example 3 - validity and satisfiability

# %%
print("P or not P valid:", is_valid(lambda m: m["P"] or not m["P"], ["P"]))
print("P and not P satisfiable:", is_satisfiable(lambda m: m["P"] and not m["P"], ["P"]))

# %% [markdown]
# ## Example 4 - forward chaining

# %%
rules = [(["Holiday"], "Closed"), (["Closed"], "Canteen"), (["Rain", "Closed"], "StayHome")]
derived, fired = forward_chain(rules, {"Holiday"})
print("derived:", sorted(derived), "rules fired:", fired)

# %% [markdown]
# ## Example 5 - backward chaining

# %%
ok, steps = backward_chain(rules, {"Holiday"}, "Canteen")
print("Canteen proved:", ok, "goals examined:", steps)
print("StayHome proved:", backward_chain(rules, {"Holiday"}, "StayHome")[0])

# %% [markdown]
# ## Example 6 - performance computation

# %%
for n in [4, 8, 12, 16]:
    t0 = time.perf_counter(); c = count_models(n)
    print(f"n={n:2d} models={c:6d} time={time.perf_counter() - t0:.4f}s")
