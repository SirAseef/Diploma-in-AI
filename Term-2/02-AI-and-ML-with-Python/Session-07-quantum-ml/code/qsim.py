"""A tiny state-vector quantum simulator and quantum-ML helpers (original code, Session 07).
Qubit 0 is the most significant bit of the basis index."""
import numpy as np

H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
X = np.array([[0, 1], [1, 0]], dtype=complex)
I2 = np.eye(2)


def ry(theta):
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    return np.array([[c, -s], [s, c]], dtype=complex)


def rz(theta):
    return np.array([[np.exp(-1j * theta / 2), 0], [0, np.exp(1j * theta / 2)]])


def zero_state(n):
    s = np.zeros(2 ** n, dtype=complex); s[0] = 1
    return s


def apply(gate, state, target, n):
    op = np.array([[1.0]])
    for q in range(n):
        op = np.kron(op, gate if q == target else I2)
    return op @ state


def cnot(state, control, target, n):
    out = state.copy()
    for i in range(2 ** n):
        if (i >> (n - 1 - control)) & 1:
            j = i ^ (1 << (n - 1 - target))
            if i < j:
                out[i], out[j] = state[j], state[i]
    return out


def probabilities(state):
    return np.abs(state) ** 2


def measure(state, shots=1000, seed=0):
    n = int(np.log2(len(state)))
    rng = np.random.default_rng(seed)
    p = probabilities(state); p = p / p.sum()
    outcomes = rng.choice(len(state), size=shots, p=p)
    counts = {}
    for o in outcomes:
        k = format(o, f"0{n}b"); counts[k] = counts.get(k, 0) + 1
    return dict(sorted(counts.items()))


def feature_map(x):
    s = zero_state(2)
    s = apply(H, s, 0, 2); s = apply(H, s, 1, 2)
    s = apply(rz(2 * x[0]), s, 0, 2); s = apply(rz(2 * x[1]), s, 1, 2)
    s = cnot(s, 0, 1, 2)
    s = apply(rz(2 * (np.pi - x[0]) * (np.pi - x[1])), s, 1, 2)
    s = cnot(s, 0, 1, 2)
    s = apply(ry(x[0]), s, 0, 2); s = apply(ry(x[1]), s, 1, 2)
    return s


def quantum_kernel(A, B):
    SA = np.array([feature_map(a) for a in A]); SB = np.array([feature_map(b) for b in B])
    return np.abs(SA.conj() @ SB.T) ** 2


def vqc_prob(x, theta):
    """Encode x, apply trainable RY layer + CNOT + RY layer, return P(qubit 1 = |1>)."""
    s = zero_state(2)
    s = apply(ry(x[0]), s, 0, 2); s = apply(ry(x[1]), s, 1, 2)
    s = apply(ry(theta[0]), s, 0, 2); s = apply(ry(theta[1]), s, 1, 2)
    s = cnot(s, 0, 1, 2)
    s = apply(ry(theta[2]), s, 0, 2); s = apply(ry(theta[3]), s, 1, 2)
    p = probabilities(s)
    return p[1] + p[3]


def vqc_loss(theta, X, y):
    p = np.clip([vqc_prob(x, theta) for x in X], 1e-9, 1 - 1e-9)
    return float(np.mean((p - y) ** 2))


def train_vqc(X, y, epochs=40, lr=0.5, seed=0):
    theta = np.random.default_rng(seed).uniform(0, np.pi, 4); losses = []
    for _ in range(epochs):
        grad = np.zeros_like(theta)
        for i in range(len(theta)):
            sh = np.zeros_like(theta); sh[i] = np.pi / 2
            # parameter-shift rule applied to each prediction, then chain rule for the squared error
            gp = np.array([(vqc_prob(x, theta + sh) - vqc_prob(x, theta - sh)) / 2 for x in X])
            p = np.array([vqc_prob(x, theta) for x in X])
            grad[i] = np.mean(2 * (p - y) * gp)
        theta -= lr * grad
        losses.append(vqc_loss(theta, X, y))
    return theta, losses
