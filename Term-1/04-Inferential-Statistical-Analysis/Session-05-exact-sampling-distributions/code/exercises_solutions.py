"""Session 05 - Practice exercise solutions."""
import numpy as np
from scipy import stats

if __name__ == "__main__":
    crit = {df: round(stats.t.ppf(0.975, df), 3) for df in (4, 14, 60)}
    print("t critical values:", crit, "vs 1.96")
    assert crit[4] == 2.776 and crit[14] == 2.145 and crit[60] > 1.96

    res = stats.chisquare([72, 48])
    print(f"coin: chi2 = {res.statistic:.2f}, p = {res.pvalue:.4f}")
    assert np.isclose(res.statistic, 4.8) and res.pvalue < 0.05

    chi2, p, dof, exp = stats.chi2_contingency([[40, 60], [25, 125]])
    print("expected:\n", exp.round(1), f"\nchi2 = {chi2:.2f}, p = {p:.5f}")
    assert dof == 1 and np.allclose(exp, [[26, 74], [39, 111]])

    p_tail = stats.f.sf(3.33, 5, 10)
    print("P(F(5,10) > 3.33) =", round(p_tail, 4))
    assert abs(p_tail - 0.05) < 0.002
    print("All exercise checks passed")
