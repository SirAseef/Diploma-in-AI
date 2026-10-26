"""Real-life problem: Student Result Calculator GUI. Run: python problem_solution.py"""
# build: no-run (opens a desktop window; logic tested in test_logic.py)
import tkinter as tk
from tkinter import messagebox
from result_logic import validate_marks, compute_result


class ResultApp(tk.Tk):
    SUBJECTS = ["Python", "SQL", "Statistics"]

    def __init__(self):
        super().__init__()
        self.title("Student Result Calculator")
        form = tk.Frame(self, padx=10, pady=10)
        form.pack(side="left")
        self.name = tk.StringVar()
        tk.Label(form, text="Name").grid(row=0, column=0, sticky="e")
        tk.Entry(form, textvariable=self.name).grid(row=0, column=1)
        self.marks = []
        for i, subject in enumerate(self.SUBJECTS, start=1):
            var = tk.StringVar()
            self.marks.append(var)
            tk.Label(form, text=subject).grid(row=i, column=0, sticky="e")
            tk.Entry(form, textvariable=var, width=8).grid(row=i, column=1, sticky="w")
        tk.Button(form, text="Calculate", command=self.calculate).grid(row=4, column=0, pady=8)
        tk.Button(form, text="Clear", command=self.clear).grid(row=4, column=1)
        self.output = tk.Label(form, text="", fg="navy")
        self.output.grid(row=5, column=0, columnspan=2)
        self.history = tk.Listbox(self, width=32)
        self.history.pack(side="right", padx=10, pady=10)

    def calculate(self):
        try:
            marks = validate_marks(v.get() for v in self.marks)
        except ValueError as e:
            messagebox.showerror("Invalid marks", str(e))
            return
        total, pct, grade = compute_result(marks)
        self.output.config(text=f"Total {total:.0f} - {pct}% - Grade {grade}")
        self.history.insert("end", f"{self.name.get() or 'Student'}: {pct}% ({grade})")

    def clear(self):
        self.name.set("")
        for v in self.marks:
            v.set("")
        self.output.config(text="")


if __name__ == "__main__":
    ResultApp().mainloop()
