"""Session 03 - Real-life problem: what drives Karachi apartment prices?"""
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf


def make_sales(n=150, seed=33):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({"size_sqft": rng.uniform(600, 2200, n).round(-1), "age_years": rng.integers(0, 30, n),
                       "floor": rng.integers(0, 10, n), "distance_to_main_road_km": rng.uniform(0.1, 3, n).round(2)})
    df["price_lakh"] = (20 + 0.11 * df["size_sqft"] - 1.1 * df["age_years"] - 6 * df["distance_to_main_road_km"]
                        + rng.normal(0, 12, n)).round(1)
    return df


def price_study(df):
    corr = df.corr()["price_lakh"].drop("price_lakh")
    best = corr.abs().idxmax()
    r, p = stats.pearsonr(df[best], df["price_lakh"])
    simple = smf.ols("price_lakh ~ size_sqft", data=df).fit()
    slope_100 = 100 * simple.params["size_sqft"]
    ci_100 = 100 * simple.conf_int().loc["size_sqft"].to_numpy()
    full = smf.ols("price_lakh ~ size_sqft + age_years + floor + distance_to_main_road_km", data=df).fit()
    significant = full.pvalues.drop("Intercept").loc[lambda s: s < 0.05].index.tolist()
    new = pd.DataFrame({"size_sqft": [1200], "age_years": [5], "floor": [3], "distance_to_main_road_km": [0.5]})
    pred = full.get_prediction(new).summary_frame(alpha=0.05)
    return best, r, p, slope_100, ci_100, full.rsquared_adj, significant, pred


if __name__ == "__main__":
    best, r, p, slope, ci, adj, sig, pred = price_study(make_sales())
    print(f"strongest: {best} (r = {r:.3f}, p = {p:.1e})")
    print(f"+100 sq ft -> +{slope:.2f} lakh (95% CI {ci[0]:.2f} to {ci[1]:.2f})")
    print(f"adjusted R2 {adj:.3f}; significant: {sig}")
    print(pred[["mean", "obs_ci_lower", "obs_ci_upper"]].round(1))
    assert best == "size_sqft" and p < 0.001
    assert ci[0] < 11 < ci[1]
    assert set(sig) == {"size_sqft", "age_years", "distance_to_main_road_km"}
    assert pred["obs_ci_lower"].iloc[0] < pred["mean"].iloc[0] < pred["obs_ci_upper"].iloc[0]
    print("All checks passed")
