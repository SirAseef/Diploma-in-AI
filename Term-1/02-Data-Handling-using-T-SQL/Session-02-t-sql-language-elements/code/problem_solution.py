"""Real-life problem: the accounts office wants a fee follow-up report.
Course fee is Rs 45,000. List students who still owe money (balance > 0), biggest balance first,
show the balance and a per-city summary of how much is outstanding."""
# notebook: run-in-code-dir
from campus_db import connect, show

FEE = 45000

OWING = """
SELECT student_id, name, COALESCE(city, 'Unknown') AS city, fee_paid, ? - fee_paid AS balance
FROM students
WHERE fee_paid < ?
ORDER BY balance DESC, name
"""

BY_CITY = """
SELECT COALESCE(city, 'Unknown') AS city, COUNT(*) AS students_owing, SUM(? - fee_paid) AS outstanding
FROM students
WHERE fee_paid < ?
GROUP BY COALESCE(city, 'Unknown')
HAVING SUM(? - fee_paid) > 0
ORDER BY outstanding DESC
"""

if __name__ == "__main__":
    con = connect()
    owing = show(con, OWING, (FEE, FEE))
    summary = show(con, BY_CITY, (FEE, FEE, FEE))
    total = sum(r[4] for r in owing)
    print("total outstanding: Rs", f"{total:,}")
    assert owing[0][4] == 45000 and len(owing) == 6
    assert total == sum(r[2] for r in summary) == 180000
    print("report OK")
