"""Session 02 - Real-life problem: hospital patients, doctors and visits (embed vs reference)."""
# notebook: run-in-code-dir
from datetime import datetime, timedelta
from mongo_conn import get_db
from schema_check import check

PATIENT_SCHEMA = {"required": ["mrn", "name", "contact"], "types": {"mrn": str, "name": str, "allergies": list, "contact": dict}}


def build_hospital(db, patients, doctors, visits):
    for p in patients:
        problems = check(p, PATIENT_SCHEMA)
        if problems:
            raise ValueError(f"{p.get('mrn')}: {problems}")
    db.patients.insert_many(patients); db.doctors.insert_many(doctors); db.visits.insert_many(visits)


def patient_card(db, mrn):
    p = db.patients.find_one({"mrn": mrn}, {"_id": 0})
    recent = list(db.visits.find({"mrn": mrn}, {"_id": 0}).sort("date", -1).limit(3))
    names = {d["_id"]: d["name"] for d in db.doctors.find({"_id": {"$in": [v["doctor_id"] for v in recent]}})}
    for v in recent:
        v["doctor"] = names[v.pop("doctor_id")]
    return {**p, "recent_visits": recent}


if __name__ == "__main__":
    db = get_db("hospital_demo")
    for c in ("patients", "doctors", "visits"):
        db[c].drop()
    patients = [
        {"mrn": "KHI-0001", "name": "Rukhsana Begum", "allergies": ["penicillin"],
         "contact": {"name": "Imran (son)", "phone": "0300-5551234"}},
        {"mrn": "KHI-0002", "name": "Tariq Mehmood", "allergies": [], "contact": {"name": "Saima (wife)", "phone": "0321-5559876"}},
    ]
    doctors = [{"_id": "D1", "name": "Dr. Farah Naz", "dept": "Cardiology"},
               {"_id": "D2", "name": "Dr. Adeel Khan", "dept": "Medicine"}]
    start = datetime(2025, 1, 5)
    visits = [{"mrn": "KHI-0001", "doctor_id": "D1" if i % 2 else "D2", "date": start + timedelta(days=30 * i),
               "reason": f"follow-up {i}"} for i in range(8)]
    visits.append({"mrn": "KHI-0002", "doctor_id": "D2", "date": datetime(2026, 9, 1), "reason": "fever"})
    build_hospital(db, patients, doctors, visits)
    card = patient_card(db, "KHI-0001")
    for k, v in card.items():
        print(f"{k}: {v}")
    assert [v["reason"] for v in card["recent_visits"]] == ["follow-up 7", "follow-up 6", "follow-up 5"]
    assert card["recent_visits"][0]["doctor"] == "Dr. Farah Naz"
    try:
        build_hospital(db, [{"mrn": "KHI-0003", "name": "No Contact"}], [], [])
        raise AssertionError("should have failed")
    except ValueError as e:
        print("rejected:", e)
    print("All checks passed")
