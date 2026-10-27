"""Session 11 practice solutions."""
import pandas as pd


def city_density():
    df = pd.DataFrame({"city": ["Karachi", "Lahore", "Islamabad", "Quetta", "Peshawar"],
                       "population": [20.4, 13.0, 1.2, 1.6, 2.3],
                       "area": [3780, 1772, 906, 3501, 1257]})
    df["density"] = (df["population"] * 1_000_000 / df["area"]).round()
    return df


def above_average_both(df):
    mask = (df["python"] > df["python"].mean()) & (df["sql"] > df["sql"].mean())
    return df.loc[mask, "name"].tolist()


def count_by_city(df):
    return df["city"].value_counts().to_dict()


def fill_by_group(df, col, group):
    out = df.copy()
    out[col] = out[col].fillna(out.groupby(group)[col].transform("mean"))
    return out


if __name__ == "__main__":
    print(city_density())
    students = pd.DataFrame({
        "name": ["Ayesha", "Bilal", "Hira", "Omar", "Zara", "Hamza"],
        "city": ["Karachi", "Lahore", "Karachi", "Quetta", "Lahore", "Karachi"],
        "python": [88, 64, 92, 50, 75, None],
        "sql": [79, 70, 95, 60, 81, 66],
    })
    print(above_average_both(students))
    assert above_average_both(students) == ["Ayesha", "Hira", "Zara"]
    assert count_by_city(students) == {"Karachi": 3, "Lahore": 2, "Quetta": 1}
    filled = fill_by_group(students, "python", "city")
    assert filled.loc[5, "python"] == 90.0       # mean of Karachi (88, 92)
    print("all checks passed")
