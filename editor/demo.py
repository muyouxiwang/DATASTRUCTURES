# -*- coding=utf-8 -*-
import re


import edit

import Tkinter as tk

def test_gui():

    root = tk.Tk()

    f = tk.Frame(root)

    global t
    t = tk.Text(f, undo=True)
    # t.edit_modified(False)
    # t.edit_reset()

    t.insert("1.0", "what is \n this")

    v = tk.StringVar()
    c = tk.Entry(f, textvariable = v)
    c.focus_set()

    def do_command(e):
        print eval(v.get())
        v.set("")

    c.bind("<Return>", do_command)

    t.pack()
    c.pack()



    f.pack()

    root.mainloop()

# t = '''def handle_special(self, special_key):'''
# p = re.compile("[a-zA-Z_]+")
# d = p.search(t)
# print d
test_gui()

