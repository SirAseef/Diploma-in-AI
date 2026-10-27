"""Session 05 - practice exercise solutions."""
# notebook: run-in-code-dir
import sqlite3
from campus_db import connect, show

con = connect()
# 1. Add a new teacher and assign them to the ML-2701 batch
con.execute("INSERT INTO faculty (faculty_id, name, subject, salary, hired_on) VALUES (6, 'Rabia Anwar', 'ML', 190000, '2026-10-01')")
con.execute("UPDATE batches SET faculty_id = 6, timing = 'Morning' WHERE batch_id = 'ML-2701'")
ex1 = show(con, "SELECT batch_id, faculty_id, timing FROM batches WHERE batch_id = 'ML-2701'")

# 2. Place student 110 in batch AI-2602 and record a payment of 20,000
con.execute("UPDATE students SET batch_id = 'AI-2602', fee_paid = fee_paid + 20000 WHERE student_id = 110")
ex2 = show(con, "SELECT batch_id, fee_paid FROM students WHERE student_id = 110")

# 3. Delete marks of subjects that no current faculty teaches (here: none should go), return count
n3 = con.execute("DELETE FROM marks WHERE subject NOT IN (SELECT subject FROM faculty)").rowcount
print("deleted rows:", n3)

# 4. Inside a transaction, give every unpaid student a 'pending' email placeholder, check, then roll back
con.execute("BEGIN")
changed = con.execute("UPDATE students SET email = 'pending@campus.pk' WHERE fee_paid = 0 AND email IS NULL").rowcount
con.execute("ROLLBACK")
ex4 = show(con, "SELECT COUNT(*) FROM students WHERE email = 'pending@campus.pk'")

if __name__ == "__main__":
    assert ex1 == [("ML-2701", 6, "Morning")]
    assert ex2 == [("AI-2602", 20000)]
    assert n3 == 0
    assert ex4 == [(0,)]
    print("all exercise checks passed")
