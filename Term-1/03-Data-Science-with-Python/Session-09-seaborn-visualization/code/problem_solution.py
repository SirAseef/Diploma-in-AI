"""Session 09 - Real-life problem: ride-hailing trips exploratory report with Seaborn."""
# notebook: run-in-code-dir
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path


def make_trips(n=600, seed=21):
    rng = np.random.default_rng(seed)
    vehicle = rng.choice(["bike", "rickshaw", "car"], n, p=[0.45, 0.3, 0.25])
    rate = pd.Series(vehicle).map({"bike": 28, "rickshaw": 45, "car": 70}).to_numpy()
    hour = rng.integers(0, 24, n)
    distance = rng.gamma(3, 2.2, n).clip(1, 35)
    rain = rng.random(n) < 0.2
    surge = 1 + 0.35 * rain + 0.15 * ((hour >= 17) & (hour <= 20))
    fare = (80 + rate * distance * surge * rng.normal(1, 0.06, n)).round(0)
    rating = (4.6 - 0.02 * distance + rng.normal(0, 0.25, n)).clip(1, 5).round(1)
    return pd.DataFrame({"hour": hour, "distance_km": distance.round(1), "fare": fare,
                         "rating": rating, "vehicle": vehicle, "rain": rain})


def trips_report(df, path):
    sns.set_theme(style="whitegrid")
    d = df.assign(fare_per_km=df["fare"] / df["distance_km"])
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), layout="constrained")
    sns.histplot(data=d, x="fare", hue="vehicle", element="step", ax=axes[0, 0])
    sns.boxplot(data=d, x="vehicle", y="fare_per_km", hue="rain", ax=axes[0, 1])
    sns.heatmap(d[["hour", "distance_km", "fare", "rating", "fare_per_km"]].corr(),
                annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=axes[1, 0])
    sns.lineplot(data=d, x="hour", y="fare", hue="vehicle", ax=axes[1, 1])
    fig.suptitle("Ride-hailing trips report (synthetic data)")
    fig.savefig(path, dpi=105); plt.close(fig)
    med = d.groupby("vehicle")["fare_per_km"].median()
    by_rain = d.groupby("rain")["fare_per_km"].median()
    return med.idxmax(), round(100 * (by_rain[True] / by_rain[False] - 1), 1)


if __name__ == "__main__":
    out = Path("output"); out.mkdir(exist_ok=True)
    best, rain_pct = trips_report(make_trips(), out / "trips_report.png")
    print("highest median fare/km:", best, "| rain uplift %:", rain_pct)
    assert best == "car"
    assert rain_pct > 15
    assert (out / "trips_report.png").exists()
    print("All checks passed")
