"""Tiny knowledge-representation toolkit for Session 05 (original code)."""


class TripleStore:
    def __init__(self):
        self.triples = set()

    def add(self, s, p, o):
        self.triples.add((s, p, o))

    def query(self, s=None, p=None, o=None):
        return sorted(t for t in self.triples
                      if (s is None or t[0] == s) and (p is None or t[1] == p) and (o is None or t[2] == o))

    def one(self, s, p):
        hits = self.query(s, p)
        return hits[0][2] if hits else None

    def transitive(self, s, p):
        out, todo = set(), [s]
        while todo:
            x = todo.pop()
            for _, _, o in self.query(x, p):
                if o not in out:
                    out.add(o); todo.append(o)
        return out


class SemanticNet:
    def __init__(self):
        self.parent, self.props = {}, {}

    def add_isa(self, child, parent):
        node = parent
        while node:
            if node == child:
                raise ValueError("is_a cycle")
            node = self.parent.get(node)
        self.parent[child] = parent

    def set(self, node, prop, value):
        self.props.setdefault(node, {})[prop] = value

    def get(self, node, prop):
        while node:
            if prop in self.props.get(node, {}):
                return self.props[node][prop]
            node = self.parent.get(node)
        return None


class Frame:
    def __init__(self, name, parent=None, **slots):
        self.name, self.parent, self.slots = name, parent, slots

    def __getitem__(self, slot):
        f = self
        while f:
            if slot in f.slots:
                return f.slots[slot]
            f = f.parent
        raise KeyError(slot)


def forward_chain(facts, rules):
    facts = set(facts)
    changed = True
    while changed:
        changed = False
        for conds, concl in rules:
            if conds <= facts and concl not in facts:
                facts.add(concl); changed = True
    return facts


def is_subclass(cls, ancestor, onto):
    while cls:
        if cls == ancestor:
            return True
        cls = onto.get(cls)
    return False
