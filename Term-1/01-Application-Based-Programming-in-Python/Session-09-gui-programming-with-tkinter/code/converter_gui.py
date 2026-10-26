"""Unit converter GUI that uses converter_logic. Run: python converter_gui.py"""
# build: no-run (opens a desktop window)
import tkinter as tk
from tkinter import ttk
from converter_logic import RATES, convert


def main():
    root = tk.Tk()
    root.title("Unit converter")
    value = tk.StringVar()
    unit = tk.StringVar(value=list(RATES)[0])
    out = tk.StringVar(value="Result appears here")

    tk.Entry(root, textvariable=value, width=12).grid(row=0, column=0, padx=8, pady=8)
    ttk.Combobox(root, textvariable=unit, values=list(RATES), state="readonly", width=14).grid(row=0, column=1)

    def on_convert():
        try:
            out.set(f"{convert(float(value.get()), unit.get()):.3f}")
        except ValueError:
            out.set("Please enter a number")

    tk.Button(root, text="Convert", command=on_convert).grid(row=0, column=2, padx=8)
    tk.Label(root, textvariable=out, fg="navy").grid(row=1, column=0, columnspan=3, pady=8)
    root.mainloop()


if __name__ == "__main__":
    main()
