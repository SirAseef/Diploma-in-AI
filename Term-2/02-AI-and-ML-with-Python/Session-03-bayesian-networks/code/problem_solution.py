"""Session 03 - Real-life problem: dengue triage Bayesian network learned from records."""
# notebook: run-in-code-dir
from bn import BayesNet, learn_cpt

STRUCTURE = [("Monsoon", []), ("Flu", []), ("Dengue", ["Monsoon"]),
             ("Fever", ["Dengue", "Flu"]), ("LowPlatelets", ["Dengue"])]


def true_network():
    net = BayesNet()
    net.add("Monsoon", [], {(): 0.3})
    net.add("Flu", [], {(): 0.15})
    net.add("Dengue", ["Monsoon"], {(True,): 0.12, (False,): 0.02})
    net.add("Fever", ["Dengue", "Flu"], {(True, True): 0.98, (True, False): 0.95, (False, True): 0.8, (False, False): 0.05})
    net.add("LowPlatelets", ["Dengue"], {(True,): 0.85, (False,): 0.04})
    return net


def learn(records):
    learned = BayesNet()
    for node, parents in STRUCTURE:
        learned.add(node, parents, learn_cpt(records, node, parents, alpha=1))
    return learned


if __name__ == "__main__":
    truth = true_network()
    records = truth.sample_df(4000, seed=5)
    print(records.mean().round(3).to_dict())
    model = learn(records)
    q1 = {"Monsoon": True, "Fever": True}; q2 = dict(q1, LowPlatelets=True)
    for q in (q1, q2):
        lp, tp = model.query("Dengue", q)[True], truth.query("Dengue", q)[True]
        print(f"P(Dengue | {q}) learned={lp:.3f} true={tp:.3f}")
        assert abs(lp - tp) < 0.05
    assert model.query("Dengue", q2)[True] > model.query("Dengue", q1)[True]
    print("OK")
