"""Session 06 - Real-life problem: rule-based loan screening agent and its performance."""
# notebook: run-in-code-dir
import numpy as np
from logic import forward_chain

RULES = [(["salaried", "good_credit"], "low_risk"), (["low_risk", "income_ok"], "approve"),
         (["defaulted"], "high_risk"), (["high_risk"], "reject")]


def make_applicants(n=200, seed=6):
    rng = np.random.default_rng(seed)
    apps, truth = [], []
    for _ in range(n):
        a = {"salaried": rng.random() < 0.6, "good_credit": rng.random() < 0.55,
             "income_ok": rng.random() < 0.7, "defaulted": rng.random() < 0.1}
        policy = a["salaried"] and a["good_credit"] and a["income_ok"] and not a["defaulted"]
        if rng.random() < 0.08:          # hidden policy is noisy: officers sometimes overrule
            policy = not policy
        apps.append(a); truth.append(int(policy))
    return apps, np.array(truth)


def decide(applicant):
    facts = {k for k, v in applicant.items() if v}
    derived, fired = forward_chain(RULES, facts)
    return int("approve" in derived and "reject" not in derived), fired


def evaluate(apps, truth):
    preds, fired = zip(*(decide(a) for a in apps))
    preds = np.array(preds)
    tp = int(((preds == 1) & (truth == 1)).sum()); fp = int(((preds == 1) & (truth == 0)).sum())
    fn = int(((preds == 0) & (truth == 1)).sum())
    return {"accuracy": float((preds == truth).mean()), "precision": tp / (tp + fp), "recall": tp / (tp + fn),
            "avg_rules_fired": float(np.mean(fired))}


if __name__ == "__main__":
    apps, truth = make_applicants()
    m = evaluate(apps, truth)
    print({k: round(v, 3) for k, v in m.items()})
    assert 0.85 < m["accuracy"] < 1.0
    assert m["precision"] > 0.7 and m["recall"] > 0.6
    print("OK")
