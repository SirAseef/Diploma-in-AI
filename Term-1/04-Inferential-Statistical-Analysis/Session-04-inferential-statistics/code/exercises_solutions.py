"""Session 04 - Practice exercise solutions."""
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportion_confint, proportions_ztest

if __name__ == "__main__":
    se = 6 / np.sqrt(36); tcrit = stats.t.ppf(0.975, 35)
    ci = (32 - tcrit * se, 32 + tcrit * se)
    ci2 = stats.t.interval(0.95, 35, loc=32, scale=se)
    assert np.allclose(ci, ci2)
    print("delivery CI:", np.round(ci, 2))

    rng = np.random.default_rng(5)
    packets = rng.normal(98.8, 2, 20)
    t, p = stats.ttest_1samp(packets, 100)
    print(f"biscuits: t = {t:.2f}, p = {p:.4f}")

    lo, hi = proportion_confint(540, 1200, method="normal")
    z, pz = proportions_ztest(540, 1200, value=0.5)
    print(f"bus route: 95% CI ({lo:.3f}, {hi:.3f}), z = {z:.2f}, p = {pz:.5f}")
    assert hi < 0.5 and pz < 0.01

    false_alarms = np.mean([stats.ttest_1samp(rng.normal(50, 10, 30), 50).pvalue < 0.05 for _ in range(2000)])
    print("Type I error rate:", false_alarms)
    assert 0.035 < false_alarms < 0.065
    print("All exercise checks passed")
