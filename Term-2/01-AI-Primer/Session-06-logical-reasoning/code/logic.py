"""Propositional logic helpers for Session 06 (original code)."""
import itertools


def implies(p, q):
    return (not p) or q


def models(symbols):
    for values in itertools.product([True, False], repeat=len(symbols)):
        yield dict(zip(symbols, values))


def entails(kb, alpha, symbols):
    return all(alpha(m) for m in models(symbols) if kb(m))


def is_valid(sentence, symbols):
    return all(sentence(m) for m in models(symbols))


def is_satisfiable(sentence, symbols):
    return any(sentence(m) for m in models(symbols))


def forward_chain(rules, facts):
    """rules: list of (premises, conclusion). Returns (derived facts, number of rule firings)."""
    facts, fired, changed = set(facts), 0, True
    while changed:
        changed = False
        for prem, concl in rules:
            if concl not in facts and all(p in facts for p in prem):
                facts.add(concl); fired += 1; changed = True
    return facts, fired


def backward_chain(rules, facts, goal, _seen=None, _steps=None):
    """Returns (proved, steps) where steps counts goals examined."""
    seen = set() if _seen is None else _seen
    steps = [0] if _steps is None else _steps
    steps[0] += 1
    if goal in facts:
        return True, steps[0]
    if goal in seen:
        return False, steps[0]
    seen.add(goal)
    for prem, concl in rules:
        if concl == goal and all(backward_chain(rules, facts, p, seen, steps)[0] for p in prem):
            return True, steps[0]
    return False, steps[0]


def count_models(n):
    return sum(1 for _ in itertools.product([True, False], repeat=n))
