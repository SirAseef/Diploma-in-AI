"""Session 05 - Practice exercise solutions."""
# notebook: run-in-code-dir
from kb import Frame, SemanticNet, TripleStore, forward_chain


def ex1():
    kb = TripleStore()
    for c, p in [("Lahore", "Punjab"), ("Multan", "Punjab"), ("Faisalabad", "Punjab"),
                 ("Karachi", "Sindh"), ("Peshawar", "Khyber Pakhtunkhwa")]:
        kb.add(c, "located_in", p)
    return [s for s, _, _ in kb.query(None, "located_in", "Punjab")]


def ex2():
    net = SemanticNet(); net.add_isa("ostrich", "bird"); net.add_isa("eagle", "bird")
    net.set("bird", "can_fly", True); net.set("ostrich", "can_fly", False)
    return net.get("ostrich", "can_fly"), net.get("eagle", "can_fly")


def ex3():
    vehicle = Frame("Vehicle", wheels=4); rickshaw = Frame("Rickshaw", parent=vehicle, wheels=3)
    return vehicle["wheels"], rickshaw["wheels"]


def ex4():
    rules = [({"fever", "cough"}, "flu_suspected"), ({"flu_suspected", "short_breath"}, "see_doctor"),
             ({"see_doctor", "age_over_60"}, "urgent")]
    start = {"fever", "cough", "short_breath", "age_over_60"}
    return forward_chain(start, rules) - start


if __name__ == "__main__":
    print("ex1", ex1()); assert ex1() == ["Faisalabad", "Lahore", "Multan"]
    print("ex2", ex2()); assert ex2() == (False, True)
    print("ex3", ex3()); assert ex3() == (4, 3)
    print("ex4", sorted(ex4())); assert ex4() == {"flu_suspected", "see_doctor", "urgent"}
    print("all exercises OK")
