"""Session 03 - practice exercise solutions."""
# notebook: run-in-code-dir
from campus_db import connect, show

con = connect()
# 1. Salary band for each faculty member: >= 200k Senior, >= 165k Mid, else Junior
ex1 = show(con, """SELECT name, salary,
    CASE WHEN salary >= 200000 THEN 'Senior' WHEN salary >= 165000 THEN 'Mid' ELSE 'Junior' END AS band
    FROM faculty ORDER BY salary DESC""")
# 2. Show 'Assigned' or 'Unassigned' for each batch's faculty
ex2 = show(con, "SELECT batch_id, IIF(faculty_id IS NULL, 'Unassigned', 'Assigned') AS status FROM batches")
# 3. Count students per fee status in one row: cleared, partial, unpaid
ex3 = show(con, """SELECT SUM(CASE WHEN fee_paid >= 45000 THEN 1 ELSE 0 END) AS cleared,
                          SUM(CASE WHEN fee_paid > 0 AND fee_paid < 45000 THEN 1 ELSE 0 END) AS partial,
                          SUM(CASE WHEN fee_paid = 0 THEN 1 ELSE 0 END) AS unpaid
                   FROM students""")
# 4. Display a contact line: email if present, otherwise 'call office', with name in capitals
ex4 = show(con, "SELECT UPPER(name) || ' - ' || COALESCE(email, 'call office') AS contact_line FROM students")

if __name__ == "__main__":
    assert [r[2] for r in ex1] == ["Senior", "Mid", "Mid", "Mid", "Junior"]
    assert ("ML-2701", "Unassigned") in ex2
    assert ex3[0] == (4, 4, 2)
    assert "BILAL AHMED - call office" in [r[0] for r in ex4]
    print("all exercise checks passed")
