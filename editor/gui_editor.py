# -*- coding=utf-8 -*-

import Tkinter as tk

import edit

root = tk.Tk()

f = tk.Frame(root)

t = tk.Text(f)

t.insert("1.0", edit.get_content())



t.tag_config("highstring", background="yellow")

highs = set()
def do(e):
    s = c.get("1.0", "1.end").encode("utf-8")
    searched = edit.search(s)
    for item in highs:
        if item not in searched:
            t.tag_remove("highstring",
            item[0], item[1])

    highs.clear()
    for i, j in searched:
        x = "%d.%d" % (i+1, j),
        y ="%d.%d" % (i+1, j + len(s.decode("utf-8")))
        t.tag_add("highstring", x, y)
        highs.add((x, y))
            


c = tk.Text(f, height=3)
c.bind("<KeyRelease>", do)

t.pack()
c.pack()
f.pack()

root.mainloop()






