# -*- coding=utf-8 -*-
import re


import edit

import Tkinter as tk

def test_gui():

    root = tk.Tk()

    f = tk.Frame(root)


    t = tk.Text(f)

    t.insert("1.0", edit.get_content())

    v = tk.StringVar()
    c = tk.Entry(f, textvariable = v)
    c.focus_set()

    def do_command(e):
        eval(v.get())
        v.set("")

    c.bind("<Return>", do_command)

    t.pack()
    c.pack()



    f.pack()

    root.mainloop()

t = '''def handle_special(self, special_key):'''
p = re.compile("[a-zA-Z_]+")
d = p.search(t)
print d

