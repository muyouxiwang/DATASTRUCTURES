# -*- coding=utf-8 -*-





import Tkinter as tk


name = "gui_catalog" 

root = tk.Tk()

f = tk.Frame(root)


t = tk.Text(f)

v = tk.StringVar()
c = tk.Entry(f, textvariable = v)
c.focus_set()

def do_command(e):
    eval(v.get())

c.bind("<Return>", do_command)

t.pack()
c.pack()



f.pack()

root.mainloop()

