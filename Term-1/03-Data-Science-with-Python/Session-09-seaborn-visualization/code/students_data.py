"""Synthetic student dataset shared by the Session 09 scripts (no internet needed)."""
import numpy as np
import pandas as pd


def make_students(n=300, seed=9):
    rng = np.random.default_rng(seed)
    campus = rng.choice(["North Nazimabad", "Gulshan", "Clifton"], n, p=[0.4, 0.35, 0.25])
    gender = rng.choice(["F", "M"], n)
    programme = rng.choice(["Data Science", "Web Dev", "AI", "Networking"], n, p=[0.35, 0.3, 0.2, 0.15])
    study = rng.gamma(4, 1.5, n).clip(0.5, 20)
    attendance = rng.normal(82, 9, n).clip(40, 100)
    sleep = rng.normal(7, 1, n).clip(4, 10)
    bonus = pd.Series(campus).map({"North Nazimabad": 3, "Gulshan": 0, "Clifton": -2}).to_numpy()
    score = (12 + 2.8 * study + 0.35 * attendance + 1.2 * sleep + bonus + rng.normal(0, 7, n)).clip(0, 100)
    return pd.DataFrame({"campus": campus, "gender": gender, "programme": programme,
                         "study_hours": study.round(1), "attendance": attendance.round(1),
                         "sleep": sleep.round(1), "score": score.round(1)})
