"""Sample 'campus' data for the MongoDB module (original, synthetic).

seed(db) drops and refills three collections:
  students  - nested marks, an array of skills, optional fields (some students have no phone)
  batches   - one document per batch with an embedded faculty sub-document
  payments  - fee payments referencing students by student_id
Returns a dict of document counts.
"""
from datetime import datetime

STUDENTS = [
    # (student_id, name, city, batch, python, sql, stats, skills, phone?, enrolled)
    (1, "Ali Raza", "Karachi", "DS-01", 78, 65, 70, ["python", "pandas"], True, "2026-01-10"),
    (2, "Sana Khan", "Lahore", "DS-01", 92, 88, 85, ["python", "sql", "tableau"], True, "2026-01-12"),
    (3, "Hamza Ali", "Karachi", "DS-02", 55, 48, 60, ["excel"], False, "2026-03-02"),
    (4, "Ayesha Noor", "Islamabad", "DS-02", 81, 90, 77, ["sql", "power bi"], True, "2026-03-05"),
    (5, "Bilal Ahmed", "Karachi", "AI-01", 67, 72, 58, ["python", "tensorflow"], True, "2026-02-01"),
    (6, "Zoya Hussain", "Hyderabad", "AI-01", 88, 70, 91, ["python", "pytorch", "sql"], False, "2026-02-03"),
    (7, "Usman Tariq", "Karachi", "DS-01", 45, 52, 40, [], True, "2026-01-15"),
    (8, "Hina Shah", "Lahore", "AI-01", 73, 81, 69, ["python", "mongodb"], True, "2026-02-07"),
    (9, "Faraz Iqbal", "Karachi", "DS-02", 95, 93, 89, ["python", "sql", "mongodb", "spark"], True, "2026-03-01"),
    (10, "Mariam Javed", "Quetta", "AI-01", 60, 58, 66, ["excel", "python"], False, "2026-02-10"),
]

BATCHES = [
    {"_id": "DS-01", "programme": "Data Science", "start": datetime(2026, 1, 10), "room": 4,
     "faculty": {"name": "Aseef Ahmed", "subject": "Python"}, "capacity": 25},
    {"_id": "DS-02", "programme": "Data Science", "start": datetime(2026, 3, 1), "room": 2,
     "faculty": {"name": "Nadia Malik", "subject": "Statistics"}, "capacity": 20},
    {"_id": "AI-01", "programme": "Artificial Intelligence", "start": datetime(2026, 2, 1), "room": 6,
     "faculty": {"name": "Kamran Siddiqui", "subject": "Machine Learning"}, "capacity": 30},
]

PAYMENTS = [  # (student_id, amount, month, method)
    (1, 15000, "2026-01", "cash"), (1, 15000, "2026-02", "bank"), (2, 15000, "2026-01", "bank"),
    (2, 15000, "2026-02", "bank"), (3, 12000, "2026-03", "easypaisa"), (4, 12000, "2026-03", "jazzcash"),
    (5, 18000, "2026-02", "bank"), (6, 18000, "2026-02", "cash"), (6, 18000, "2026-03", "cash"),
    (8, 18000, "2026-02", "easypaisa"), (9, 12000, "2026-03", "bank"), (9, 12000, "2026-04", "bank"),
]


def student_docs():
    docs = []
    for sid, name, city, batch, py, sql, st, skills, phone, enrolled in STUDENTS:
        d = {"student_id": sid, "name": name, "city": city, "batch": batch,
             "marks": {"python": py, "sql": sql, "stats": st}, "skills": skills,
             "enrolled": datetime.fromisoformat(enrolled)}
        if phone:
            d["phone"] = f"0300-{1000000 + sid * 1111:07d}"
        docs.append(d)
    return docs


def seed(db):
    for name in ("students", "batches", "payments"):
        db[name].drop()
    db.students.insert_many(student_docs())
    db.batches.insert_many([dict(b) for b in BATCHES])
    db.payments.insert_many([{"student_id": s, "amount": a, "month": m, "method": me} for s, a, m, me in PAYMENTS])
    return {n: db[n].count_documents({}) for n in ("students", "batches", "payments")}


if __name__ == "__main__":
    from mongo_conn import get_db
    print(seed(get_db("campus_check")))
