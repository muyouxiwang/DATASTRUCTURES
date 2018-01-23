# -*- coding=utf-8 -*-

import Tkinter as tk

import edit
import editor_status


class GuiEditor(tk.Tk):
    def __init__(self, content):
        tk.Tk.__init__(self)



        f = tk.Frame(self)
        f.pack()

        self.t = tk.Text(f)
        self.t.insert("1.0", content)

        self.t.pack()
        self.t.mark_set("insert", "1.0")

        #self.c = tk.Text(f, height=3)
        self.v = tk.StringVar()
        self.c = tk.Entry(f, textvariable = self.v)


        self.d = tk.Entry(f)


        self.l = tk.Label(f)

        self.t.pack()

        self.l.pack()



        self.t.tag_config("highlight", background="yellow")


        self.cur_status = editor_status.NormalStatus(self, self.t)


    def remove_highlight(self, index1, index2 = None):
        self.t.tag_remove("highlight", index1, index2)

    def add_highlight(self, index1, index2 = None):
        self.t.tag_add("highlight", index1, index2)

    def set_insert_index(self, index):
        self.t.mark_set("insert", index)

    def add_select_region(self, index1, index2 = None):
        self.t.tag_add("sel", index1, index2)

    def focus_index(self, index):
        self.t.see(index)

    def move_visual_cursor(self, toindex):
        self.remove_highlight("insert")
        self.set_insert_index(toindex)
        self.add_highlight("insert")
        


    def set_label(self, info):
        self.l.config(text = info)

    def start(self):
        self.mainloop()


GuiEditor(edit.get_content()).start()



