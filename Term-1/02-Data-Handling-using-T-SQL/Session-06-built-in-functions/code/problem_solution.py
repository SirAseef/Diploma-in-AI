"""Real-life problem: monthly batch performance report (like the one a centre's academic manager sends).
For each student with marks: batch, average, rank inside the batch, gap to the batch topper,
percentile band, days since joining and a clean display name. Then a one-line summary per batch."""
# notebook: run-in-code-dir
from campus_db import connect, show

TODAY = "2026-10-27"

REPORT = """
WITH avg_marks AS (
    SELECT s.student_id, s.name, s.batch_id, s.joined_on, ROUND(AVG(m.marks), 1) AS avg_marks
    FROM students s JOIN marks m ON m.student_id = s.student_id
    WHERE s.batch_id IS NOT NULL
    GROUP BY s.student_id, s.name, s.batch_id, s.joined_on
)
SELECT batch_id,
       UPPER(SUBSTR(name, INSTR(name, ' ') + 1)) || ', ' || SUBSTR(name, 1, INSTR(name, ' ') - 1) AS display_name,
       avg_marks,
       RANK() OVER (PARTITION BY batch_id ORDER BY avg_marks DESC)              AS batch_rank,
       ROUND(MAX(avg_marks) OVER (PARTITION BY batch_id) - avg_marks, 1)         AS gap_to_top,
       CASE NTILE(3) OVER (ORDER BY avg_marks DESC) WHEN 1 THEN 'Top third'
            WHEN 2 THEN 'Middle third' ELSE 'Bottom third' END                   AS band,
       CAST(julianday(?) - julianday(joined_on) AS INTEGER)                      AS days_enrolled
FROM avg_marks
ORDER BY batch_id, batch_rank
"""

SUMMARY = """
SELECT s.batch_id,
       COUNT(DISTINCT s.student_id)                         AS students,
       ROUND(AVG(m.marks), 1)                               AS batch_avg,
       MAX(m.marks)                                         AS best_mark,
       group_concat(DISTINCT CASE WHEN m.marks < 50 THEN s.name END) AS needs_support
FROM students s JOIN marks m ON m.student_id = s.student_id
GROUP BY s.batch_id
ORDER BY batch_avg DESC
"""

if __name__ == "__main__":
    con = connect()
    report = show(con, REPORT, (TODAY,))
    summary = show(con, SUMMARY)
    top_ai2601 = [r for r in report if r[0] == "AI-2601"][0]
    assert top_ai2601[1] == "KHAN, Ayesha" and top_ai2601[3] == 1 and top_ai2601[4] == 0
    assert len(report) == 9
    assert summary[0][0] == "AI-2602" and "Ali Raza" in summary[-1][4]
    print("batch report OK")
