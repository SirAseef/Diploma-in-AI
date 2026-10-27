"""Session 03 - Real-life problem: warehouse shelves (blocks world) formulation."""
# notebook: run-in-code-dir
from problems import Problem, explore


class Shelves(Problem):
    def actions(self, s):
        return [(i, j) for i in range(3) for j in range(3) if i != j and s[i]]

    def result(self, s, a):
        i, j = a
        shelves = [list(x) for x in s]
        shelves[j].append(shelves[i].pop())
        return tuple(tuple(x) for x in shelves)


if __name__ == "__main__":
    prob = Shelves((("A", "B", "C"), (), ()), goal=((), (), ("A", "B", "C")))
    print("actions at start:", prob.actions(prob.initial))
    states = explore(prob)
    print("reachable states:", len(states))
    assert prob.goal in states
    assert len(states) == 60  # 3 boxes on 3 ordered stacks
    print("goal reachable: True")
