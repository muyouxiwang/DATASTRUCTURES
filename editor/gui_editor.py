# -*- coding=utf-8 -*-

import Tkinter as tk
import ttk

import edit
import editor_status


class Scrollbar(ttk.Scrollbar):
    def set(self, first, last):
        if float(first) <= 0.0 and float(last) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        ttk.Scrollbar.set(self, first, last)

class GuiEditor(tk.Tk):
    def __init__(self, content):
        tk.Tk.__init__(self)



        self.clipboard = ""


        f = tk.Frame(self)

        self.t = tk.Text(f, wrap=tk.NONE)
        self.t.insert("1.0", content)

        self.t.pack()
        self.t.mark_set("insert", "1.0")

        #self.c = tk.Text(f, height=3)
        self.v = tk.StringVar()
        self.c = tk.Entry(f, textvariable = self.v)


        self.d = tk.Entry(f)


        self.l = tk.Label(f)




        self.t.tag_config("highlight", background="yellow")

        self.t.tag_config("syntax_blue", background="blue")


        self.cur_status = editor_status.NormalStatus(self, self.t)


        self.t.bind("<KeyPress>", self.handle_keypress)
        self.t.bind("<Escape>", self.back_to_normal)


        self.y_scroll = Scrollbar(f, orient = tk.VERTICAL)
        self.x_scroll = Scrollbar(f, orient = tk.HORIZONTAL)
        self.t['yscrollcommand'] = self.y_scroll.set
        self.t['xscrollcommand'] = self.x_scroll.set
        self.y_scroll['command'] = self.t.yview
        self.x_scroll['command'] = self.t.xview
        self.y_scroll.grid(row = 0, column = 1, sticky = tk.N+tk.S, rowspan = 2)
        self.x_scroll.grid(row = 1, column = 0, sticky = tk.E+tk.W, rowspan = 2)
        self.t.grid(row = 0, column = 0, sticky = tk.N+tk.S+tk.E+tk.W)

        #self.t.pack()

        self.l.grid()

        f.pack()

    def syntax(self, e):
        self.t.search


    def back_to_normal(self, e):
        self.cur_status.handle_escape()
        return "break"

    def handle_keypress(self, e):
        print "keychar is(%s), keycode is (%s)" % (e.char, e.keycode)

        self.cur_status.handle_keypress(e.char)


    def remove_highlight(self, index1, index2 = None):
        self.t.tag_remove("highlight", index1, index2)

    def add_highlight(self, index1, index2 = None):
        self.t.tag_add("highlight", index1, index2)

    def set_insert_index(self, index):
        self.t.mark_set("insert", index)

    def add_select_region(self, index1, index2, line_mode = False):
        if self.t.compare(index1, ">", index2):
            index1, index2 = index2, index1
        if line_mode:
            index1 += " linestart"
            index2 += " lineend"
        self.t.tag_add("sel", index1, index2)
    
    def get_select_region(self):
        try: return self.t.get("sel.first", "sel.last")
        except: return ""

    def add_text(self, index, text):
        print "shit !!!!!!!!!!"
        self.t.insert(index, text)

    def remove_all_select_region(self):
# 去掉v模式下的高亮选择，没有选中的情况下会报错，所以用try
        try: self.t.tag_remove("sel", "sel.first", "sel.last")
        except: pass

    def focus_index(self, index):
        self.t.see(index)

    def move_visual_cursor(self, toindex, direc = "S"):
        self.remove_highlight("insert")
        self.set_insert_index(toindex)
        self.add_highlight("insert")


        if self.t.bbox(toindex) is None:
            if direc == "N":
                self.t.yview_scroll(-2, tk.UNITS)
            if direc == "S":
                self.t.yview_scroll(2, tk.UNITS)
            if direc == "W":
                self.t.xview_scroll(-2, tk.UNITS)
            if direc == "E":
                self.t.xview_scroll(2, tk.UNITS)
            
        if self.t.bbox(toindex) is None:
            self.t.see(toindex)

    def get_insert_index(self):
        return self.t.index("insert")

    def get_win_top_index(self):
        cur_line = int(float(self.t.index("insert")))
        while cur_line > 0:
            cur_line -= 1
            if self.t.bbox("%d.0" % cur_line) is None:
                return "%d.0" % (cur_line + 1)
        return "%d.0" % cur_line

    def get_win_bottom_index(self):
        cur_line = int(float(self.t.index("insert")))
        max_line = int(float(self.t.index("end")))
        while cur_line < max_line:
            cur_line += 1
            if self.t.bbox("%d.0" % cur_line) is None:
                return "%d.0" % (cur_line - 1)
        return "%d.0" % cur_line
        

        


    def set_label(self, info):
        self.l.config(text = info)

    def start(self):
        self.mainloop()


GuiEditor(edit.get_content()).start()



