"""Small search library for Session 04 (original code)."""
import heapq
import itertools
import math
from collections import deque

from problems import Problem


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0.0):
        self.state, self.parent, self.action, self.path_cost = state, parent, action, path_cost

    def path_states(self):
        n, out = self, []
        while n:
            out.append(n.state); n = n.parent
        return out[::-1]

    def path_actions(self):
        n, out = self, []
        while n.parent:
            out.append(n.action); n = n.parent
        return out[::-1]


def expand(problem, node):
    for a in problem.actions(node.state):
        s2 = problem.result(node.state, a)
        yield Node(s2, node, a, node.path_cost + problem.action_cost(node.state, a, s2))


def breadth_first(problem, stats=None):
    stats = {} if stats is None else stats; stats["expanded"] = 0
    node = Node(problem.initial)
    if problem.is_goal(node.state): return node
    frontier, reached = deque([node]), {problem.initial}
    while frontier:
        node = frontier.popleft(); stats["expanded"] += 1
        for child in expand(problem, node):
            if problem.is_goal(child.state): return child
            if child.state not in reached:
                reached.add(child.state); frontier.append(child)
    return None


def depth_first(problem, stats=None):
    stats = {} if stats is None else stats; stats["expanded"] = 0
    frontier, reached = [Node(problem.initial)], {problem.initial}
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state): return node
        stats["expanded"] += 1
        for child in expand(problem, node):
            if child.state not in reached:
                reached.add(child.state); frontier.append(child)
    return None


def best_first(problem, f, stats=None):
    stats = {} if stats is None else stats; stats["expanded"] = 0
    node = Node(problem.initial); counter = itertools.count()
    frontier, reached = [(f(node), next(counter), node)], {problem.initial: node}
    while frontier:
        _, _, node = heapq.heappop(frontier)
        if node is not reached[node.state]:
            continue  # stale entry: a cheaper path to this state was found later
        if problem.is_goal(node.state): return node
        stats["expanded"] += 1
        for child in expand(problem, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child; heapq.heappush(frontier, (f(child), next(counter), child))
    return None


def uniform_cost(problem, stats=None):
    return best_first(problem, lambda n: n.path_cost, stats)


def astar(problem, h, stats=None):
    return best_first(problem, lambda n: n.path_cost + h(n), stats)


def greedy(problem, h, stats=None):
    return best_first(problem, h, stats)


class RouteProblem(Problem):
    def __init__(self, initial, goal, roads, coords):
        super().__init__(initial, goal)
        self.coords, self.graph = coords, {}
        for (a, b), d in roads.items():
            self.graph.setdefault(a, {})[b] = d; self.graph.setdefault(b, {})[a] = d

    def actions(self, s): return list(self.graph[s])
    def result(self, s, a): return a
    def action_cost(self, s, a, s2): return self.graph[s][s2]

    def h(self, node):
        (x1, y1), (x2, y2) = self.coords[node.state], self.coords[self.goal]
        return math.dist((x1, y1), (x2, y2))


# Approximate road distances (km) and planar coordinates (km grid), simplified for teaching.
ROADS = {("Karachi", "Hyderabad"): 165, ("Hyderabad", "Sukkur"): 320, ("Karachi", "Sukkur"): 470,
         ("Sukkur", "Multan"): 450, ("Multan", "Lahore"): 340, ("Multan", "Faisalabad"): 240,
         ("Faisalabad", "Lahore"): 185, ("Faisalabad", "Islamabad"): 310, ("Lahore", "Islamabad"): 375,
         ("Islamabad", "Peshawar"): 185, ("Sukkur", "Dera Ismail Khan"): 520,
         ("Dera Ismail Khan", "Peshawar"): 320, ("Multan", "Dera Ismail Khan"): 240}
COORDS = {"Karachi": (0, 0), "Hyderabad": (120, 110), "Sukkur": (150, 400), "Multan": (450, 700),
          "Faisalabad": (600, 850), "Lahore": (750, 850), "Islamabad": (560, 1120),
          "Peshawar": (400, 1150), "Dera Ismail Khan": (300, 800)}


def misplaced(node, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
    return sum(1 for a, b in zip(node.state, goal) if a and a != b)


def manhattan(node, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
    total = 0
    for i, t in enumerate(node.state):
        if t:
            j = goal.index(t)
            total += abs(i // 3 - j // 3) + abs(i % 3 - j % 3)
    return total
