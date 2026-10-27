"""Session 04 - Practice exercise solutions."""
# notebook: run-in-code-dir
from problems import EightPuzzle, WaterJug
from search import COORDS, ROADS, RouteProblem, astar, breadth_first, greedy, manhattan, uniform_cost


def ex1():
    return breadth_first(WaterJug((5, 3), 4)).path_actions()


def ex2():
    roads = dict(ROADS); roads[("Sukkur", "Quetta")] = 390
    coords = dict(COORDS); coords["Quetta"] = (-150, 600)
    n = uniform_cost(RouteProblem("Karachi", "Quetta", roads, coords))
    return n.path_states(), n.path_cost


def ex3():
    p = RouteProblem("Peshawar", "Karachi", ROADS, COORDS)
    start = (7, 2, 4, 5, 0, 6, 8, 3, 1)
    puzzle = (len(greedy(EightPuzzle(start), manhattan).path_actions()),
              len(astar(EightPuzzle(start), manhattan).path_actions()))
    return greedy(p, p.h).path_cost, astar(p, p.h).path_cost, puzzle


def ex4():
    start = (1, 2, 3, 4, 5, 6, 7, 8, 0); p = EightPuzzle(start)
    moves = ["U", "L", "U", "L", "D", "R", "D", "R", "U", "U", "L", "D"]
    for m in moves: start = p.result(start, m)
    s1, s2 = {}, {}
    a = breadth_first(EightPuzzle(start), stats=s1); b = astar(EightPuzzle(start), manhattan, stats=s2)
    return len(b.path_actions()), s1["expanded"], s2["expanded"], len(a.path_actions())


if __name__ == "__main__":
    plan = ex1(); print("ex1", plan); assert len(plan) == 6
    path, cost = ex2(); print("ex2", path, cost); assert path[-1] == "Quetta" and cost == 860
    g, a, (pg, pa) = ex3(); print("ex3 map greedy:", g, "A*:", a, "| puzzle greedy:", pg, "A*:", pa)
    assert a <= g and pa < pg  # same on the small map, greedy far worse on the puzzle
    depth, bfs_n, astar_n, bfs_len = ex4(); print("ex4 depth", depth, "BFS", bfs_n, "A*", astar_n)
    assert depth == bfs_len and astar_n < bfs_n
    print("all exercises OK")
