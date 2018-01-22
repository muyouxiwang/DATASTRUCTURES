# -*- coding=utf-8 -*-
import Tkinter as tk

import edit

root = tk.Tk()


f = tk.Frame(root)

t = tk.Text(f)


def get_refresh(p):
    def _(e):
        if p in edit.the_catalog:
            edit.the_catalog[p].toggle()
            show()
    return _
        

def show():
    t.config(cursor = "arrow",
            #insertwidth = 10,
            insertbackground = "brown")
    t.delete("1.0", tk.END)
    i = 1
    for n, p in edit.root.get_series():
        t.insert("%d.0" % i, n)
        t.tag_add(p, "%d.0" % i, "%d.%d" % (i, len(n)))
        i += 1

        t.tag_bind(p, '<Button-1>', get_refresh(p))

        if n.strip().startswith("+"):
            t.tag_config(p, foreground = "red")
        if n.strip().startswith("*"):
            t.tag_config(p, foreground = "blue")



show()

t.pack()
f.pack()

root.mainloop()



