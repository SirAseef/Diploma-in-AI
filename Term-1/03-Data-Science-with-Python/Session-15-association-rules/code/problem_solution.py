"""Session 15 - Real-life problem: grocery-store rules and a cart recommender."""
# notebook: run-in-code-dir
import numpy as np
from apriori import association_rules, frequent_itemsets, show, to_basket


def make_receipts(n=1000, seed=15):
    rng = np.random.default_rng(seed)
    base = {"bread": 0.30, "eggs": 0.25, "milk": 0.40, "chai": 0.30, "sugar": 0.20, "rice": 0.20,
            "daal": 0.18, "oil": 0.15, "biscuits": 0.20, "soap": 0.10}
    receipts = []
    for _ in range(n):
        t = {i for i, p in base.items() if rng.random() < p}
        if "chai" in t and rng.random() < 0.6: t.add("rusk")
        if "bread" in t and rng.random() < 0.55: t.add("eggs")
        if "rice" in t and rng.random() < 0.6: t.add("daal")
        if {"rice", "daal"} <= t and rng.random() < 0.5: t.add("oil")
        if not t: t.add("biscuits")
        receipts.append(sorted(t))
    return receipts


def store_rules(transactions, min_support=0.04, min_confidence=0.4):
    basket = to_basket(transactions)
    fi = frequent_itemsets(basket, min_support)
    multi = fi[fi["itemset"].map(len) >= 2]
    rules = association_rules(fi, min_confidence)
    top5 = rules[rules["lift"] > 1].nlargest(5, "lift")
    return multi, rules, top5


def recommend(cart, rules, n=3):
    cart = set(cart)
    usable = rules[rules["antecedent"].map(lambda a: a <= cart) & (rules["lift"] > 1)]
    scores = {}
    for _, r in usable.iterrows():
        for item in r["consequent"] - cart:
            scores[item] = max(scores.get(item, 0), r["lift"] * r["confidence"])
    return sorted(scores, key=scores.get, reverse=True)[:n]


if __name__ == "__main__":
    receipts = make_receipts()
    multi, rules, top5 = store_rules(receipts)
    print(len(multi), "frequent pairs/triples;", len(rules), "rules")
    show(top5)
    rec_rice = recommend(["rice"], rules)
    rec_chai = recommend(["chai", "milk"], rules)
    print("cart [rice] ->", rec_rice, "| cart [chai, milk] ->", rec_chai)
    assert any(len(s) == 3 for s in multi["itemset"])
    assert rec_rice[0] == "daal"
    assert "rusk" in rec_chai
    assert (top5["lift"] > 1).all() and (top5["confidence"] >= 0.4).all()
    print("All checks passed")
