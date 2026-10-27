"""Session 06 - Real-life problem: which courier partner is fastest?"""
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multicomp import pairwise_tukeyhsd


def make_deliveries(seed=66):
    rng = np.random.default_rng(seed)
    base = {"A": 30, "B": 26, "C": 31}
    weekend = {"A": 6, "B": 2, "C": 7}
    rows = [(c, d, base[c] + (weekend[c] if d == "weekend" else 0) + rng.normal(0, 4))
            for c in base for d in ("weekday", "weekend") for _ in range(30)]
    return pd.DataFrame(rows, columns=["courier", "day_type", "hours"])


def courier_study(df, alpha=0.05):
    groups = [g["hours"].to_numpy() for _, g in df.groupby("courier")]
    f, p = stats.f_oneway(*groups)
    one = smf.ols("hours ~ C(courier)", data=df).fit()
    table = sm.stats.anova_lm(one, typ=2)
    eta_sq = table.loc["C(courier)", "sum_sq"] / table["sum_sq"].sum()
    checks = {"levene_p": stats.levene(*groups).pvalue, "shapiro_p": stats.shapiro(one.resid).pvalue}
    tukey = pairwise_tukeyhsd(df["hours"], df["courier"], alpha=alpha)
    tk = pd.DataFrame(tukey.summary().data[1:], columns=tukey.summary().data[0])
    different = tk.loc[tk["reject"].astype(bool), ["group1", "group2"]].apply(tuple, axis=1).tolist()
    two = sm.stats.anova_lm(smf.ols("hours ~ C(courier) * C(day_type)", data=df).fit(), typ=2)
    p_interaction = two.loc["C(courier):C(day_type)", "PR(>F)"]
    p_kw = stats.kruskal(*groups).pvalue
    best = df.groupby("courier")["hours"].mean().idxmin()
    return p, eta_sq, checks, different, p_interaction, p_kw, best


if __name__ == "__main__":
    df = make_deliveries()
    print(df.groupby(["courier", "day_type"])["hours"].mean().unstack().round(1))
    p, eta, checks, diff, p_int, p_kw, best = courier_study(df)
    print(f"one-way p = {p:.2e}, eta^2 = {eta:.2f}, checks = { {k: round(v, 3) for k, v in checks.items()} }")
    print("pairs that differ:", diff)
    print(f"interaction p = {p_int:.4f}, Kruskal-Wallis p = {p_kw:.2e} -> recommend courier {best}")
    assert p < 0.001 and p_kw < 0.001 and eta > 0.14
    assert ("A", "B") in diff and ("B", "C") in diff and ("A", "C") not in diff
    assert p_int < 0.05
    assert best == "B"
    print("All checks passed")
