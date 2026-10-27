"""Tiny Bayesian-network toolkit for binary variables (original code, Session 03)."""
import itertools
import numpy as np
import pandas as pd


class BayesNet:
    def __init__(self):
        self.nodes, self.parents, self.cpt = [], {}, {}

    def add(self, node, parents, cpt):
        """cpt maps a tuple of parent values to P(node=True)."""
        for p in parents:
            assert p in self.parents, f"add parent {p} before {node}"
        self.nodes.append(node); self.parents[node] = list(parents); self.cpt[node] = dict(cpt)

    def prob(self, node, value, world):
        p_true = self.cpt[node][tuple(world[p] for p in self.parents[node])]
        return p_true if value else 1 - p_true

    def joint(self, world):
        out = 1.0
        for n in self.nodes:
            out *= self.prob(n, world[n], world)
        return out

    def query(self, X, evidence):
        hidden = [n for n in self.nodes if n != X and n not in evidence]
        dist = {}
        for x in (True, False):
            total = 0.0
            for values in itertools.product((True, False), repeat=len(hidden)):
                world = dict(evidence, **dict(zip(hidden, values))); world[X] = x
                total += self.joint(world)
            dist[x] = total
        z = dist[True] + dist[False]
        return {k: v / z for k, v in dist.items()}

    def sample(self, rng):
        world = {}
        for n in self.nodes:
            world[n] = bool(rng.random() < self.prob(n, True, world))
        return world

    def sample_df(self, n, seed=0):
        rng = np.random.default_rng(seed)
        return pd.DataFrame([self.sample(rng) for _ in range(n)])


def rejection_sample(net, X, evidence, n=10000, seed=0):
    rng = np.random.default_rng(seed); counts = {True: 0, False: 0}
    for _ in range(n):
        w = net.sample(rng)
        if all(w[k] == v for k, v in evidence.items()):
            counts[w[X]] += 1
    z = counts[True] + counts[False]
    return {k: v / z for k, v in counts.items()} if z else None


def learn_cpt(df, node, parents, alpha=1):
    """Estimate P(node=True | parents) with Laplace smoothing alpha."""
    cpt = {}
    for values in itertools.product((True, False), repeat=len(parents)):
        sub = df
        for p, v in zip(parents, values):
            sub = sub[sub[p] == v]
        cpt[values] = (sub[node].sum() + alpha) / (len(sub) + 2 * alpha)
    return cpt


def example_net():
    net = BayesNet()
    net.add("Summer", [], {(): 0.4})
    net.add("UncleTesting", [], {(): 0.05})
    net.add("LoadShedding", ["Summer"], {(True,): 0.7, (False,): 0.2})
    net.add("GeneratorOn", ["LoadShedding", "UncleTesting"],
            {(True, True): 0.99, (True, False): 0.9, (False, True): 0.95, (False, False): 0.02})
    net.add("UPSBeeps", ["LoadShedding"], {(True,): 0.8, (False,): 0.05})
    return net
