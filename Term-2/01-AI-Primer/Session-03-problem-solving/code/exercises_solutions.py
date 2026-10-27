"""Session 03 - Practice exercise solutions."""
# notebook: run-in-code-dir
from problems import EightPuzzle, WaterJug, explore

PEAS = {"Performance": "student marks improve, time well used", "Environment": "students, question bank, syllabus",
        "Actuators": "show question, show hint", "Sensors": "submitted answers, time taken"}


def ex2():
    return explore(WaterJug(caps=(5, 3), target=4))


def misplaced(state, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
    return sum(1 for a, b in zip(state, goal) if a and a != b)


CHESS = {"observable": "fully", "deterministic": "deterministic", "episodic": "sequential",
         "static": "semi-dynamic (clock runs)", "discrete": "discrete"}

if __name__ == "__main__":
    print("ex1", PEAS); assert len(PEAS) == 4
    states = ex2(); print("ex2 states:", len(states)); assert any(4 in s for s in states)
    h = misplaced((1, 2, 3, 4, 0, 6, 7, 5, 8)); print("ex3 misplaced:", h); assert h == 2
    assert misplaced(EightPuzzle((1, 2, 3, 4, 5, 6, 7, 8, 0)).initial) == 0
    print("ex4", CHESS)
    print("all exercises OK")
