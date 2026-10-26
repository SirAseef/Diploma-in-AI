"""Session 09 - a tour of common widgets and layouts. Run: python widgets_tour.py"""
# build: no-run (opens a desktop window)
import tkinter as tk
from tkinter import messagebox, ttk


def main():
    root = tk.Tk()
    root.title("Widgets tour")
    root.geometry("420x360")

    # pack: header
    tk.Label(root, text="Assalam-o-Alaikum!", font=("Segoe UI", 14, "bold")).pack(pady=8)

    # grid inside a Frame: a small form
    form = tk.Frame(root, padx=10)
    form.pack()
    entries = {}
    for row, label in enumerate(["Name", "Email"]):
        tk.Label(form, text=label).grid(row=row, column=0, sticky="e", padx=5, pady=3)
        entries[label] = tk.Entry(form, width=25)
        entries[label].grid(row=row, column=1)
    course = ttk.Combobox(form, values=["Python", "SQL", "MongoDB"], state="readonly", width=22)
    course.current(0)
    tk.Label(form, text="Course").grid(row=2, column=0, sticky="e", padx=5)
    course.grid(row=2, column=1, pady=3)

    shift = tk.StringVar(value="Morning")
    for i, s in enumerate(["Morning", "Evening"]):
        tk.Radiobutton(form, text=s, variable=shift, value=s).grid(row=3, column=i)
    newsletter = tk.BooleanVar()
    tk.Checkbutton(form, text="Send me updates", variable=newsletter).grid(row=4, column=0, columnspan=2)

    result = tk.Label(root, text="", fg="navy")

    def greet():
        name = entries["Name"].get().strip() or "stranger"
        result.config(text=f"Hello, {name}! {course.get()} · {shift.get()} · updates={newsletter.get()}")

    tk.Button(root, text="Greet", command=greet).pack(pady=6)
    result.pack()
    tk.Button(root, text="About", command=lambda: messagebox.showinfo("About", "Diploma in AI · Session 09")).pack(pady=6)
    root.mainloop()


if __name__ == "__main__":
    main()
