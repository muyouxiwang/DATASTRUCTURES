# -*- coding=utf-8 -*-

import Tkinter as tk

import edit

root = tk.Tk()

f = tk.Frame(root)

t = tk.Text(f)

t.insert("1.0", edit.get_content())

#t.config(state = tk.DISABLED)



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
            

def change_to_v_status():
    #print t.get("sel.first", "sel.last")
    t.config(state = "disabled")
    t.tag_add("highstring", "insert", "insert + 1c")


def move_down(e):
    #print dir(e)
    #t.tag_add("sel", "sel.first+5 lines", "sel.last+1 lines")
    t.tag_remove("highstring", "insert")#, "insert + 1c")
    t.mark_set("insert", "insert + 1 lines")
    t.tag_add("highstring", "insert")#, "insert + 1 lines + 1c")
    print t.get("insert", "insert + 1c")

def move_right(e):
    t.tag_remove("highstring", "insert")#, "insert + 1c")
    t.mark_set("insert", "insert + 1c")
    t.tag_add("highstring", "insert")#, "insert + 1 lines + 1c")
    print t.get("insert", "insert + 1c")

def move_up(e):
    t.tag_remove("highstring", "insert")#, "insert + 1c")
    t.mark_set("insert", "insert - 1 lines")
    t.tag_add("highstring", "insert")#, "insert + 1 lines + 1c")
    print t.get("insert", "insert + 1c")

def move_left(e):
    t.tag_remove("highstring", "insert")#, "insert + 1c")
    t.mark_set("insert", "insert - 1c")
    t.tag_add("highstring", "insert")#, "insert + 1 lines + 1c")
    print t.get("insert", "insert + 1c")

    

t.bind("<KeyPress-j>", move_down)
t.bind("<KeyPress-k>", move_up)
t.bind("<KeyPress-h>", move_left)
t.bind("<KeyPress-l>", move_right)


c = tk.Text(f, height=3)
c.bind("<KeyRelease>", do)
b = tk.Button(f, text="change_v", command = change_to_v_status)

t.pack()
c.pack()
b.pack()
f.pack()

root.mainloop()






