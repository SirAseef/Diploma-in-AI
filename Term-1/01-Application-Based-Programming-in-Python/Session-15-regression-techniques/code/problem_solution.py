"""Real-life problem: forecast a household's monthly electricity bill (K-Electric style units)
from weather and usage, compare regression techniques and pick the best by test error."""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler


def make_bills(n=400, seed=3):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "avg_temp_c": rng.uniform(18, 40, n).round(1),
        "ac_units": rng.integers(0, 4, n),
        "family_size": rng.integers(2, 9, n),
        "load_shedding_hrs": rng.uniform(0, 8, n).round(1),
    })
    cooling = np.maximum(df.avg_temp_c - 26, 0) ** 2 * df.ac_units * 1.6     # AC kicks in above 26 °C
    df["units_kwh"] = (120 + 25 * df.family_size + cooling - 12 * df.load_shedding_hrs
                       + rng.normal(0, 25, n)).round()
    return df


def compare(df):
    X, y = df.drop(columns="units_kwh"), df["units_kwh"]
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0)
    models = {
        "Linear": make_pipeline(StandardScaler(), LinearRegression()),
        "Polynomial (deg 2) + Ridge": make_pipeline(PolynomialFeatures(2), StandardScaler(), Ridge(alpha=1)),
        "Random forest": RandomForestRegressor(n_estimators=300, random_state=0),
    }
    rows = []
    for name, model in models.items():
        p = model.fit(X_tr, y_tr).predict(X_te)
        rows.append({"model": name, "MAE_kwh": round(mean_absolute_error(y_te, p), 1), "R2": round(r2_score(y_te, p), 3)})
    table = pd.DataFrame(rows).sort_values("MAE_kwh").reset_index(drop=True)
    best = models[table.loc[0, "model"]]
    return table, best


if __name__ == "__main__":
    bills = make_bills()
    table, best = compare(bills)
    print(table.to_string(index=False))
    july = pd.DataFrame([{"avg_temp_c": 36, "ac_units": 2, "family_size": 5, "load_shedding_hrs": 2}])
    print("forecast for a hot July month:", int(best.predict(july)[0]), "kWh")
    assert table.loc[0, "model"] != "Linear"          # the curved AC effect beats a straight line
    print("comparison OK")
