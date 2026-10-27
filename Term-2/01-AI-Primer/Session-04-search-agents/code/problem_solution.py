"""Session 04 - Real-life problem: fastest rider route in a housing-society grid with A*."""
# notebook: run-in-code-dir
from problems import Problem
from search import astar, uniform_cost


class GridRoute(Problem):
    def __init__(self, start, goal, walls, size=8):
        super().__init__(start, goal); self.walls, self.size = set(walls), size

    def actions(self, s):
        x, y = s
        steps = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [p for p in steps if 0 <= p[0] < self.size and 0 <= p[1] < self.size and p not in self.walls]

    def result(self, s, a):
        return a

    def action_cost(self, s, a, s2):
        return 0.5 if s2[0] == 3 else 1.0

    def h(self, node):
        return 0.5 * (abs(node.state[0] - self.goal[0]) + abs(node.state[1] - self.goal[1]))


WALLS = [(1, 1), (1, 2), (1, 3), (2, 3), (5, 2), (5, 3), (5, 4), (5, 5), (6, 5), (4, 6), (4, 7)]

if __name__ == "__main__":
    prob = GridRoute((0, 0), (7, 6), WALLS)
    sa, su = {}, {}
    a = astar(prob, prob.h, sa); u = uniform_cost(prob, su)
    print("A* route:", a.path_states()); print("minutes:", a.path_cost)
    print("expanded  A*:", sa["expanded"], " UCS:", su["expanded"])
    assert a.path_cost == u.path_cost, "A* with admissible h must match UCS cost"
    # The 0.5-scaled heuristic is weak (needed for admissibility), so the saving is small here.
    print("A* saving vs UCS:", su["expanded"] - sa["expanded"], "nodes")
    assert not set(a.path_states()) & set(WALLS)
    print("OK")
