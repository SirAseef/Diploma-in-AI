"""Session 03 - Bayesian Networks: worked examples."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - define the network and CPTs (see bn.example_net)

# %%
from bn import example_net, learn_cpt, rejection_sample

net = example_net()
for n in net.nodes:
    print(n, "parents:", net.parents[n], "CPT:", net.cpt[n])

# %% [markdown]
# ## Example 2 - joint probability of one full world

# %%
world = {"Summer": True, "UncleTesting": False, "LoadShedding": True, "GeneratorOn": True, "UPSBeeps": True}
print("P(world) =", round(net.joint(world), 5))

# %% [markdown]
# ## Example 3 - diagnostic query by enumeration

# %%
print("P(LoadShedding):", round(net.query("LoadShedding", {})[True], 3))
print("P(LoadShedding | GeneratorOn):", round(net.query("LoadShedding", {"GeneratorOn": True})[True], 3))

# %% [markdown]
# ## Example 4 - explaining away

# %%
print("P(LoadShedding | GeneratorOn, UncleTesting):",
      round(net.query("LoadShedding", {"GeneratorOn": True, "UncleTesting": True})[True], 3))

# %% [markdown]
# ## Example 5 - rejection sampling

# %%
approx = rejection_sample(net, "LoadShedding", {"GeneratorOn": True}, n=20000, seed=0)
print("sampled estimate:", round(approx[True], 3))

# %% [markdown]
# ## Example 6 - learn CPTs from data

# %%
df = net.sample_df(5000, seed=1)
learned = learn_cpt(df, "GeneratorOn", ["LoadShedding", "UncleTesting"])
for k, v in learned.items():
    print(k, "learned", round(v, 3), "true", net.cpt["GeneratorOn"][k])
