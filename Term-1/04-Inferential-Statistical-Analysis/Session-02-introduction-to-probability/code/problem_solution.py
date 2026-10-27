"""Session 02 - Real-life problem: call-centre staffing with Poisson and Bayes."""
import numpy as np
from scipy import stats


def call_centre(rate=6, p_angry=0.15, hang_angry=0.6, hang_calm=0.10, target=0.05):
    calls = stats.poisson(rate)
    p_over_8 = calls.sf(8)
    agents = next(k for k in range(rate, 5 * rate) if calls.sf(k) < target)
    p_hang = hang_angry * p_angry + hang_calm * (1 - p_angry)
    p_angry_given_hang = hang_angry * p_angry / p_hang
    return p_over_8, agents, p_angry_given_hang


if __name__ == "__main__":
    p8, agents, p_ang = call_centre()
    print(f"P(>8 calls) = {p8:.4f} | agents needed = {agents} | P(angry | hung up) = {p_ang:.3f}")
    rng = np.random.default_rng(6)
    minutes = rng.poisson(6, 200_000)
    angry = rng.random(200_000) < 0.15
    hung = np.where(angry, rng.random(200_000) < 0.6, rng.random(200_000) < 0.10)
    print(f"simulated: P(>8) = {(minutes > 8).mean():.4f}, P(angry | hung up) = {angry[hung].mean():.3f}")
    assert abs((minutes > 8).mean() - p8) < 0.005
    assert abs(angry[hung].mean() - p_ang) < 0.01
    assert agents == 10 and stats.poisson(6).sf(9) >= 0.05
    print("All checks passed")
