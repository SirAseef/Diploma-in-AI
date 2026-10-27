"""Session 03 - Practice exercise solutions."""
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

if __name__ == "__main__":
    x = np.array([2, 4, 6, 8, 10.0]); y = np.array([3, 7, 5, 11, 14.0])
    r = ((x - x.mean()) * (y - y.mean())).sum() / np.sqrt(((x - x.mean()) ** 2).sum() * ((y - y.mean()) ** 2).sum())
    assert np.isclose(r, stats.pearsonr(x, y)[0])

    b1 = r * y.std(ddof=1) / x.std(ddof=1); b0 = y.mean() - b1 * x.mean()
    lr = stats.linregress(x, y)
    assert np.isclose(b1, lr.slope) and np.isclose(b0, lr.intercept)

    rng = np.random.default_rng(4)
    temp = rng.uniform(20, 42, 300)
    d = pd.DataFrame({"temp": temp, "ice": 10 * temp + rng.normal(0, 20, 300), "drown": 0.3 * temp + rng.normal(0, 1.5, 300)})
    raw_r = stats.pearsonr(d["ice"], d["drown"])[0]
    partial_r = stats.pearsonr(smf.ols("ice ~ temp", d).fit().resid, smf.ols("drown ~ temp", d).fit().resid)[0]
    print(f"r(ice, drown) = {raw_r:.2f}; after controlling for temperature = {partial_r:.2f}")
    assert raw_r > 0.6 and abs(partial_r) < 0.15

    ci = smf.ols("y ~ x", pd.DataFrame({"x": x, "y": y})).fit().conf_int().loc["x"]
    assert ci[0] < lr.slope < ci[1]
    print(f"r = {r:.3f}, y = {b0:.2f} + {b1:.2f}x, slope CI {ci[0]:.2f} to {ci[1]:.2f}")
    print("All exercise checks passed")
