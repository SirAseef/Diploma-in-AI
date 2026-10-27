"""Session 15 - Association rules: worked examples."""
# notebook: run-in-code-dir

# %% [markdown]
# ## Example 1 - transactions to a one-hot basket

# %%
import pandas as pd
from apriori import association_rules, frequent_itemsets, show, to_basket
transactions = [
    ["bread", "eggs", "milk"], ["bread", "butter", "eggs"], ["chai", "rusk", "milk"],
    ["chai", "rusk", "sugar"], ["bread", "eggs"], ["chai", "milk", "sugar"],
    ["bread", "butter", "milk"], ["chai", "rusk"], ["bread", "eggs", "butter"], ["coke", "chips"],
]
basket = to_basket(transactions)
print(basket.astype(int))

# %% [markdown]
# ## Example 2 - support by hand

# %%
support = basket.mean()
print(support.sort_values(ascending=False))
pair = (basket["bread"] & basket["eggs"]).mean()
print("support{bread, eggs} =", pair)

# %% [markdown]
# ## Example 3 - confidence and lift by hand

# %%
conf = pair / support["bread"]
lift = conf / support["eggs"]
print(f"bread -> eggs: confidence {conf:.2f}, lift {lift:.2f}")
assert round(conf, 2) == 0.8 and round(lift, 2) == 2.0

# %% [markdown]
# ## Example 4 - frequent itemsets with our Apriori

# %%
fi = frequent_itemsets(basket, min_support=0.2)
print(fi)

# %% [markdown]
# ## Example 5 - rules, filtered and sorted

# %%
rules = association_rules(fi, min_confidence=0.6)
show(rules[rules["lift"] > 1])

# %% [markdown]
# ## Example 6 - substitutes (lift < 1)

# %%
rules_all = association_rules(fi, min_confidence=0.0)
show(rules_all[rules_all["lift"] < 1])
