"""Session 05 - Real-life problem: exam-eligibility help-desk with triples, frames and a rule."""
# notebook: run-in-code-dir
from kb import Frame, TripleStore

PROGRAMME = Frame("Programme", min_attendance=75)
FRAMES = {"Diploma-AI": Frame("Diploma-AI", parent=PROGRAMME, min_attendance=80),
          "Certificate-Web": Frame("Certificate-Web", parent=PROGRAMME)}

kb = TripleStore()
for s, p, o in [("B-101", "of_programme", "Diploma-AI"), ("B-202", "of_programme", "Certificate-Web"),
                ("Hamza", "in_batch", "B-101"), ("Hamza", "attendance", 78), ("Hamza", "fees_cleared", True),
                ("Ayesha", "in_batch", "B-101"), ("Ayesha", "attendance", 91), ("Ayesha", "fees_cleared", True),
                ("Bilal", "in_batch", "B-202"), ("Bilal", "attendance", 78), ("Bilal", "fees_cleared", True)]:
    kb.add(s, p, o)


def min_attendance(student):
    batch = kb.one(student, "in_batch")
    programme = kb.one(batch, "of_programme")
    return FRAMES[programme]["min_attendance"]


def eligible(student):
    att = kb.one(student, "attendance"); fees = kb.one(student, "fees_cleared")
    return att >= min_attendance(student) and bool(fees)


if __name__ == "__main__":
    for st in ["Hamza", "Ayesha", "Bilal"]:
        print(f"{st}: attendance {kb.one(st, 'attendance')}%, needs {min_attendance(st)}% -> eligible={eligible(st)}")
    assert not eligible("Hamza")      # 78 < 80 for Diploma-AI
    assert eligible("Ayesha")
    assert eligible("Bilal")          # 78 >= default 75
    print("OK")
