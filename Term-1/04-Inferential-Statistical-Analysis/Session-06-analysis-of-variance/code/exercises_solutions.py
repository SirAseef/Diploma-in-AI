"""Session 06 - Practice exercise solutions."""
from itertools import combinations
import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

if __name__ == "__main__":
    groups = [np.array(g, float) for g in ([23, 25, 21, 24], [30, 28, 31, 29], [22, 26, 24, 23])]
    allx = np.concatenate(groups); grand = allx.mean()
    ssb = sum(len(g) * (g.mean() - grand) ** 2 for g in groups)
    ssw = sum(((g - g.mean()) ** 2).sum() for g in groups)
    F = (ssb / 2) / (ssw / 9)
    assert np.isclose(F, stats.f_oneway(*groups).statistic)
    print(f"SSB {ssb:.2f}, SSW {ssw:.2f}, F {F:.2f}")

    rng = np.random.default_rng(7)
    fw_t = fw_anova = 0
    for _ in range(2000):
        sims = [rng.normal(50, 10, 15) for _ in range(3)]
        fw_t += any(stats.ttest_ind(a, b).pvalue < 0.05 for a, b in combinations(sims, 2))
        fw_anova += stats.f_oneway(*sims).pvalue < 0.05
    print("family-wise error: 3 t-tests", fw_t / 2000, "| ANOVA", fw_anova / 2000)
    assert fw_t / 2000 > 0.08 and fw_anova / 2000 < 0.07

    tk = pairwise_tukeyhsd(allx, np.repeat(["g1", "g2", "g3"], 4))
    sig = [(r[0], r[1]) for r in tk.summary().data[1:] if r[-1]]
    print("Tukey significant pairs:", sig)
    assert sig == [("g1", "g2"), ("g2", "g3")]

    kw = stats.kruskal(rng.exponential(1, 30), rng.exponential(2, 30), rng.exponential(4, 30))
    print("Kruskal-Wallis p:", round(kw.pvalue, 5))
    assert kw.pvalue < 0.05
    print("All exercise checks passed")
