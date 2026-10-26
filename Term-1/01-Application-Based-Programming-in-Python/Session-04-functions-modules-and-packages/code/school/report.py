"""Report builder that re-uses the grades module."""
from .grades import letter_grade, gpa


def make_report(name, subjects):
    lines = [f"Report card: {name}"]
    for subject, marks in subjects.items():
        lines.append(f"  {subject:8} {marks:>3}  {letter_grade(marks)}")
    lines.append(f"  GPA: {gpa(list(subjects.values()))}")
    return "\n".join(lines)
