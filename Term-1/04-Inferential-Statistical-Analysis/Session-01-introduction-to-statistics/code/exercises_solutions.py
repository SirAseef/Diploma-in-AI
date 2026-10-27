"""Session 01 - Practice exercise solutions."""
import numpy as np
import pandas as pd

if __name__ == "__main__":
    s = pd.Series([12, 15, 15, 18, 20, 22, 95])
    assert (round(s.mean(), 2), s.median(), s.mode()[0]) == (28.14, 18.0, 15)

    x = np.array([3, 7, 7, 19, 24])
    var = ((x - x.mean()) ** 2).sum() / (len(x) - 1)
    assert np.isclose(var, pd.Series(x).var())

    z_maths, z_eng = (78 - 65) / 8, (70 - 60) / 5
    assert z_eng > z_maths
    print(f"z Maths {z_maths:.3f}, z English {z_eng:.3f} -> relatively better in English")

    scales = {"CNIC": "nominal", "shoe size": "ratio (discrete)", "rank": "ordinal",
              "temperature °C": "interval", "monthly rent": "ratio"}
    assert scales["temperature °C"] == "interval"
    print("All exercise checks passed")
