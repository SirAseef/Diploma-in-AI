"""Session 09 practice solutions - four small GUIs in one window (tabs).
Run: python exercises_solutions.py"""
# build: no-run (opens a desktop window; logic tested in test_logic.py)
import tkinter as tk
from tkinter import ttk
from result_logic import bmi, check_login


def counter_tab(parent):
    f = ttk.Frame(parent, padding=10)
    count = tk.IntVar(value=0)
    tk.Label(f, textvariable=count, font=("Segoe UI", 24)).pack()
    tk.Button(f, text="+1", command=lambda: count.set(count.get() + 1)).pack(side="left", padx=4)
    tk.Button(f, text="-1", command=lambda: count.set(count.get() - 1)).pack(side="left", padx=4)
    tk.Button(f, text="Reset", command=lambda: count.set(0)).pack(side="left", padx=4)
    return f


def login_tab(parent):
    f = ttk.Frame(parent, padding=10)
    user, pwd, msg = tk.StringVar(), tk.StringVar(), tk.StringVar()
    tk.Label(f, text="Username").grid(row=0, column=0)
    tk.Entry(f, textvariable=user).grid(row=0, column=1)
    tk.Label(f, text="Password").grid(row=1, column=0)
    tk.Entry(f, textvariable=pwd, show="*").grid(row=1, column=1)
    tk.Button(f, text="Login", command=lambda: msg.set(
        "Welcome!" if check_login(user.get(), pwd.get()) else "Wrong username or password")).grid(row=2, column=1)
    tk.Label(f, textvariable=msg).grid(row=3, column=0, columnspan=2)
    return f


def dark_tab(parent, root):
    f = tk.Frame(parent, padx=10, pady=10)
    dark = tk.BooleanVar()

    def toggle():
        colour = "#222222" if dark.get() else "SystemButtonFace" if root.tk.call("tk", "windowingsystem") == "win32" else "#d9d9d9"
        f.config(bg=colour)

    tk.Checkbutton(f, text="Dark mode", variable=dark, command=toggle).pack()
    return f


def bmi_tab(parent):
    f = ttk.Frame(parent, padding=10)
    w, h, out = tk.StringVar(), tk.StringVar(), tk.StringVar()
    tk.Label(f, text="Weight (kg)").grid(row=0, column=0)
    tk.Entry(f, textvariable=w).grid(row=0, column=1)
    tk.Label(f, text="Height (m)").grid(row=1, column=0)
    tk.Entry(f, textvariable=h).grid(row=1, column=1)

    def calc():
        try:
            value, cat = bmi(float(w.get()), float(h.get()))
            out.set(f"BMI {value} - {cat}")
        except (ValueError, ZeroDivisionError):
            out.set("Enter valid numbers")

    tk.Button(f, text="Calculate", command=calc).grid(row=2, column=1)
    tk.Label(f, textvariable=out).grid(row=3, column=0, columnspan=2)
    return f


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Session 09 exercises")
    tabs = ttk.Notebook(root)
    tabs.add(counter_tab(tabs), text="Counter")
    tabs.add(login_tab(tabs), text="Login")
    tabs.add(dark_tab(tabs, root), text="Dark mode")
    tabs.add(bmi_tab(tabs), text="BMI")
    tabs.pack(fill="both", expand=True)
    root.mainloop()
