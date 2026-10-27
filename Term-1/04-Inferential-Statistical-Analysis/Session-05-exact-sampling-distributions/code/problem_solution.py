"""Session 05 - Real-life problem: graduate placement, district mix and salary spread."""
import numpy as np
import pandas as pd
from scipy import stats


def placement_study(survey, district_counts, ds, web):
    table = pd.crosstab(survey["programme"], survey["placed"])
    chi2, p_ind, dof, expected = stats.chi2_contingency(table)
    contrib = ((table - expected) ** 2 / expected).round(2)
    gof = stats.chisquare(district_counts)
    F = np.var(ds, ddof=1) / np.var(web, ddof=1)
    d1, d2 = len(ds) - 1, len(web) - 1
    p_f = 2 * min(stats.f.sf(F, d1, d2), stats.f.cdf(F, d1, d2))
    p_lev = stats.levene(ds, web).pvalue
    s2 = np.var(ds, ddof=1)
    sd_ci = np.sqrt([d1 * s2 / stats.chi2.ppf(0.975, d1), d1 * s2 / stats.chi2.ppf(0.025, d1)])
    return p_ind, contrib, gof.pvalue, p_f, p_lev, sd_ci


if __name__ == "__main__":
    rng = np.random.default_rng(55)
    prog = rng.choice(["Data Science", "Web Dev", "AI", "Networking"], 400)
    rate = pd.Series(prog).map({"Data Science": 0.78, "Web Dev": 0.66, "AI": 0.72, "Networking": 0.42})
    survey = pd.DataFrame({"programme": prog, "placed": np.where(rng.random(400) < rate, "yes", "no")})
    district_counts = [128, 96, 92, 84]          # Central, East, South, Korangi
    ds = rng.normal(120, 35, 12)
    web = rng.normal(90, 12, 15)
    p_ind, contrib, p_gof, p_f, p_lev, sd_ci = placement_study(survey, district_counts, ds, web)
    print(pd.crosstab(survey["programme"], survey["placed"]))
    print("independence p =", round(p_ind, 5)); print(contrib)
    print("district GOF p =", round(p_gof, 4))
    print(f"variance F-test p = {p_f:.4f}, Levene p = {p_lev:.4f}, DS salary SD 95% CI = {sd_ci.round(1)}")
    assert p_ind < 0.01
    assert contrib.loc["Networking"].sum() == contrib.sum(axis=1).max()
    assert p_gof < 0.05
    assert p_f < 0.05 and sd_ci[0] < 35 < sd_ci[1]
    print("All checks passed")
