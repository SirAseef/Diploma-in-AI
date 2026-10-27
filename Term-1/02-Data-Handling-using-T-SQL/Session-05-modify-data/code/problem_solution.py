"""Real-life problem: nightly fee-payment import.
The bank sends a file of (student_id, amount, paid_on). Apply it safely:
- reject unknown students and non-positive amounts (log them),
- add valid amounts to students.fee_paid and keep an audit trail in fee_payments,
- do everything in ONE transaction: if anything unexpected fails, nothing is changed."""
# notebook: run-in-code-dir
import sqlite3
from campus_db import connect, show

AUDIT = """CREATE TABLE IF NOT EXISTS fee_payments (
    payment_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id  INTEGER NOT NULL REFERENCES students(student_id),
    amount      INTEGER NOT NULL CHECK (amount > 0),
    paid_on     TEXT    NOT NULL
)"""


def import_payments(con, rows):
    con.execute(AUDIT)
    known = {r[0] for r in con.execute("SELECT student_id FROM students")}
    rejected, applied = [], 0
    try:
        con.execute("BEGIN")
        for sid, amount, paid_on in rows:
            if sid not in known or amount <= 0:
                rejected.append((sid, amount, "unknown student" if sid not in known else "bad amount"))
                continue
            con.execute("INSERT INTO fee_payments (student_id, amount, paid_on) VALUES (?, ?, ?)", (sid, amount, paid_on))
            con.execute("UPDATE students SET fee_paid = fee_paid + ? WHERE student_id = ?", (amount, sid))
            applied += 1
        con.execute("COMMIT")
    except sqlite3.Error:
        con.execute("ROLLBACK")
        raise
    return applied, rejected


if __name__ == "__main__":
    con = connect()
    before = con.execute("SELECT SUM(fee_paid) FROM students").fetchone()[0]
    batch = [(102, 15000, "2026-10-26"), (106, 45000, "2026-10-26"), (999, 5000, "2026-10-26"),
             (104, -100, "2026-10-26"), (109, 15000, "2026-10-27")]
    applied, rejected = import_payments(con, batch)
    print("applied:", applied, "| rejected:", rejected)
    show(con, "SELECT s.name, s.fee_paid, COUNT(p.payment_id) AS payments FROM students s JOIN fee_payments p ON p.student_id = s.student_id GROUP BY s.name, s.fee_paid")
    after = con.execute("SELECT SUM(fee_paid) FROM students").fetchone()[0]
    assert applied == 3 and len(rejected) == 2 and after - before == 75000

    # a failing statement mid-way leaves the data untouched
    con.execute("CREATE TRIGGER no_big BEFORE INSERT ON fee_payments WHEN NEW.amount > 100000 BEGIN SELECT RAISE(ABORT, 'amount too large'); END")
    try:
        import_payments(con, [(101, 1000, "2026-10-28"), (103, 500000, "2026-10-28")])
    except sqlite3.Error as e:
        print("batch failed and was rolled back:", e)
    assert con.execute("SELECT SUM(fee_paid) FROM students").fetchone()[0] == after
    print("import OK")
