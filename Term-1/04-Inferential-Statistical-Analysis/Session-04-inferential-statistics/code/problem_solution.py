"""Session 04 - Real-life problem: did the new teaching method work?"""
import numpy as np
from scipy import stats
from statsmodels.stats.power import TTestIndPower


def ci(x, level=0.95):
    return stats.t.interval(level, len(x) - 1, loc=np.mean(x), scale=stats.sem(x))


def teaching_study(new, old, pre, post, alpha=0.05):
    ci_new, ci_old = ci(new), ci(old)
    t, p_one = stats.ttest_ind(new, old, equal_var=False, alternative="greater")
    d = (np.mean(new) - np.mean(old)) / np.sqrt((np.var(new, ddof=1) + np.var(old, ddof=1)) / 2)
    t_pair, p_pair = stats.ttest_rel(post, pre, alternative="greater")
    n_needed = TTestIndPower().solve_power(effect_size=5 / 12, power=0.8, alpha=alpha)
    return {"ci_new": tuple(np.round(ci_new, 1)), "ci_old": tuple(np.round(ci_old, 1)), "p_welch": p_one,
            "cohens_d": round(d, 2), "p_paired": p_pair, "n_per_group": int(np.ceil(n_needed))}


if __name__ == "__main__":
    rng = np.random.default_rng(44)
    old = rng.normal(64, 12, 50).clip(0, 100)
    pre = rng.normal(55, 11, 45).clip(0, 100)
    post = (pre + rng.normal(15, 6, 45)).clip(0, 100)
    new = post                                   # final marks of the new-method batch
    out = teaching_study(new, old, pre, post)
    for k, v in out.items():
        print(f"{k:>12}: {v}")
    assert out["p_welch"] < 0.05 and out["cohens_d"] > 0.3
    assert out["p_paired"] < 0.001
    assert 85 <= out["n_per_group"] <= 95       # ~ 92 per group for d = 0.417
    print("All checks passed")
