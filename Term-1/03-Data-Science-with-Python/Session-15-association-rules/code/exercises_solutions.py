"""Session 15 - Practice exercise solutions."""
# notebook: run-in-code-dir
from apriori import association_rules, frequent_itemsets, to_basket

if __name__ == "__main__":
    tx = [["chai", "rusk"], ["chai", "rusk", "milk"], ["chai", "sugar"], ["rusk"], ["chai", "rusk", "sugar"],
          ["milk", "bread"], ["chai", "milk"], ["bread", "eggs"], ["chai", "rusk", "eggs"], ["milk"]]
    basket = to_basket(tx)
    s_chai, s_rusk = basket["chai"].mean(), basket["rusk"].mean()
    s_both = (basket["chai"] & basket["rusk"]).mean()
    assert (s_chai, s_rusk, s_both) == (0.6, 0.5, 0.4)

    conf_cr, conf_rc = s_both / s_chai, s_both / s_rusk
    lift_cr, lift_rc = conf_cr / s_rusk, conf_rc / s_chai
    print(f"chai->rusk conf {conf_cr:.2f}, rusk->chai conf {conf_rc:.2f}, lift {lift_cr:.2f} both ways")
    assert abs(lift_cr - lift_rc) < 1e-12 and round(lift_cr, 3) == 1.333

    counts = {s: len(frequent_itemsets(basket, s)) for s in (0.3, 0.2, 0.1)}
    print("itemsets found:", counts)
    assert counts[0.3] < counts[0.2] < counts[0.1]

    def rules_for(rules, item):
        return rules[rules["consequent"].map(lambda c: c == frozenset([item]))]

    r = rules_for(association_rules(frequent_itemsets(basket, 0.2), 0.5), "rusk")
    assert list(r["antecedent"]) == [frozenset(["chai"])]
    print("All exercise checks passed")
