"""Session 02 - Practice exercise solutions."""
import numpy as np
from scipy import stats

if __name__ == "__main__":
    outcomes = [(a, b) for a in range(1, 7) for b in range(1, 7)]
    p7 = sum(a + b == 7 for a, b in outcomes) / 36
    rng = np.random.default_rng(0)
    sim = (rng.integers(1, 7, 200_000) + rng.integers(1, 7, 200_000) == 7).mean()
    assert np.isclose(p7, 1 / 6) and abs(sim - p7) < 0.005

    p_glasses = 0.6 * 0.3 + 0.4 * 0.2
    p_girl_given = 0.6 * 0.3 / p_glasses
    assert np.isclose(p_glasses, 0.26) and round(p_girl_given, 3) == 0.692

    p_5plus = stats.binom(10, 0.25).sf(4)
    assert round(p_5plus, 3) == 0.078

    m = stats.norm(62, 12)
    above80, cutoff = m.sf(80), m.ppf(0.9)
    print(f"P(sum=7)={p7:.3f}, P(girl|glasses)={p_girl_given:.3f}, P(>=5 guessed)={p_5plus:.3f}, "
          f"above 80: {100 * above80:.1f}%, top-10% cut-off: {cutoff:.1f}")
    assert round(100 * above80, 1) == 6.7 and round(cutoff, 1) == 77.4
    print("All exercise checks passed")
