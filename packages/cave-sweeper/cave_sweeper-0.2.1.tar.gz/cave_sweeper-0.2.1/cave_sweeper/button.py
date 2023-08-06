from tkinter import *
from tkinter import ttk


root = Tk()
selection_frame = ttk.Frame(root, padding="50 50 50 50")
selection_frame.grid(column=0, row=0, sticky=NSEW)

s = ttk.Style()
s.configure(style="Field.TButton", bd=0, pady=0, padx=0, width=2, height=2, background="gray38")
b = ttk.Button(selection_frame, text="OK", style="Field.TButton")
b.grid(row=0, column=0)
b.update()
print(b.winfo_height(), b.winfo_width(), b.winfo_geometry())

root.mainloop()
