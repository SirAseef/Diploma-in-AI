"""Shared problem definitions for Sessions 03-04 (original code)."""
from collections import deque


class Problem:
    def __init__(self, initial, goal=None):
        self.initial, self.goal = initial, goal

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def is_goal(self, state):
        return state == self.goal

    def action_cost(self, s, a, s2):
        return 1


class WaterJug(Problem):
    def __init__(self, caps=(4, 3), target=2):
        super().__init__((0, 0))
        self.cap, self.target = caps, target

    def actions(self, s):
        return ["fill A", "fill B", "empty A", "empty B", "pour A->B", "pour B->A"]

    def result(self, s, a):
        A, B = s
        cA, cB = self.cap
        if a == "fill A": return (cA, B)
        if a == "fill B": return (A, cB)
        if a == "empty A": return (0, B)
        if a == "empty B": return (A, 0)
        if a == "pour A->B":
            t = min(A, cB - B); return (A - t, B + t)
        if a == "pour B->A":
            t = min(B, cA - A); return (A + t, B - t)
        raise ValueError(a)

    def is_goal(self, s):
        return self.target in s


class EightPuzzle(Problem):
    MOVES = {"U": -3, "D": 3, "L": -1, "R": 1}

    def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
        super().__init__(tuple(initial), tuple(goal))

    def actions(self, s):
        r, c = divmod(s.index(0), 3)
        return [m for m, ok in [("U", r > 0), ("D", r < 2), ("L", c > 0), ("R", c < 2)] if ok]

    def result(self, s, a):
        i = s.index(0); j = i + self.MOVES[a]
        lst = list(s); lst[i], lst[j] = lst[j], lst[i]
        return tuple(lst)


def explore(problem):
    """Return every state reachable from problem.initial (breadth-first)."""
    seen, frontier = {problem.initial}, deque([problem.initial])
    while frontier:
        s = frontier.popleft()
        for a in problem.actions(s):
            s2 = problem.result(s, a)
            if s2 not in seen:
                seen.add(s2); frontier.append(s2)
    return seen


def run_plan(problem, plan):
    s = problem.initial; trace = [s]
    for a in plan:
        s = problem.result(s, a); trace.append(s)
    return trace
