"""A small, readable Apriori implementation with pandas (original course code).

frequent_itemsets(basket, min_support) -> DataFrame[itemset (frozenset), support]
association_rules(fi, min_confidence)  -> DataFrame[antecedent, consequent, support, confidence, lift]
"""
from itertools import combinations
import pandas as pd


def to_basket(transactions):
    items = sorted({i for t in transactions for i in t})
    return pd.DataFrame([[i in set(t) for i in items] for t in transactions], columns=items)


def _support(basket, itemset):
    return basket[list(itemset)].all(axis=1).mean()


def frequent_itemsets(basket, min_support=0.1, max_len=None):
    current = [frozenset([c]) for c in basket.columns if basket[c].mean() >= min_support]
    result = {s: _support(basket, s) for s in current}
    k = 2
    while current and (max_len is None or k <= max_len):
        prev = set(current)
        candidates = {a | b for a in current for b in current if len(a | b) == k}
        candidates = [c for c in candidates if all(frozenset(sub) in prev for sub in combinations(c, k - 1))]
        current = []
        for c in candidates:
            s = _support(basket, c)
            if s >= min_support:
                result[c] = s
                current.append(c)
        k += 1
    out = pd.DataFrame({"itemset": list(result), "support": list(result.values())})
    return out.sort_values(["support"], ascending=False, kind="stable").reset_index(drop=True)


def association_rules(fi, min_confidence=0.5):
    sup = dict(zip(fi["itemset"], fi["support"]))
    rows = []
    for itemset, s in sup.items():
        if len(itemset) < 2:
            continue
        for r in range(1, len(itemset)):
            for ante in map(frozenset, combinations(itemset, r)):
                cons = itemset - ante
                conf = s / sup[ante]
                if conf >= min_confidence:
                    rows.append({"antecedent": ante, "consequent": cons, "support": s,
                                 "confidence": conf, "lift": conf / sup[cons]})
    cols = ["antecedent", "consequent", "support", "confidence", "lift"]
    return pd.DataFrame(rows, columns=cols).sort_values("lift", ascending=False).reset_index(drop=True)


def show(rules, n=10):
    """Pretty-print rules as 'a, b -> c'."""
    for _, r in rules.head(n).iterrows():
        print(f"{', '.join(sorted(r['antecedent'])):>22} -> {', '.join(sorted(r['consequent'])):<14}"
              f" support {r['support']:.2f}  confidence {r['confidence']:.2f}  lift {r['lift']:.2f}")
