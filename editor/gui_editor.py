# -*- coding=utf-8 -*-

import Tkinter as tk
import ttk
import os

import gui
import edit
import editor_status


class Scrollbar(ttk.Scrollbar):
    def set(self, first, last):
        if float(first) <= 0.0 and float(last) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        ttk.Scrollbar.set(self, first, last)


class GuiEditor(gui.BaseEditor):
    def __init__(self, root):
        # super(GuiEditor, self).__init__(root)
        gui.BaseEditor.__init__(self, root)

        self.content = None
        self.clipboard = ""


        self.t.mark_set("insert", "1.0")

        self.c = tk.Text(self, height=1)

        self.l = tk.Label(self)


        self.t.bind("<KeyPress>", self.handle_keypress)
        self.t.bind("<Escape>", self.handle_special("escape"))
        self.t.bind("<Control-e>", self.handle_special("c_e"))
        self.t.bind("<Control-y>", self.handle_special("c_y"))

        self.c.bind("<Return>", self.handle_special("return"))
        self.c.bind("<KeyRelease>", self.handle_special("release"))
        self.c.bind("<Tab>", self.handle_special("tab"))


        self.y_scroll = Scrollbar(self, orient = tk.VERTICAL)
        self.x_scroll = Scrollbar(self, orient = tk.HORIZONTAL)
        self.t['yscrollcommand'] = self.y_scroll.set
        self.t['xscrollcommand'] = self.x_scroll.set
        self.y_scroll['command'] = self.t.yview
        self.x_scroll['command'] = self.t.xview
        self.y_scroll.grid(row = 0, column = 1, sticky = tk.N+tk.S, rowspan = 2)
        self.x_scroll.grid(row = 1, column = 0, sticky = tk.E+tk.W, rowspan = 2)
        self.t.grid(row = 0, column = 0, sticky = tk.N+tk.S+tk.E+tk.W)


        self.t.grid(sticky = tk.E+tk.W)
        self.l.grid(sticky = tk.E+tk.W)

        self.pack()

    def set_cur_status(self, status):
        self.cur_status = status
        self.set_label(status.STATUS)


    def open_new_file(self, filepath):
        if not os.path.isfile(filepath):
            self.show_warning("file not exist :%s" % filepath)
            return
        if not self.content.saved:
            self.show_warning("content allready modifyed")
            return
                
        self.set_content(edit.Content(filepath))
            

    def set_content(self, content):
        self.content = content
        self.clear_text()
        self.add_text("1.0", self.content.get_content())
        self.move_visual_cursor("1.0")
        self.t.focus_set()

    def show_warning(self, msg):
        print msg


    def clear_text(self):
        self.set_cur_status(editor_status.InsertStatus(self, self.t)) 
        self.t.delete("1.0", "end")
        self.set_cur_status(editor_status.NormalStatus(self, self.t)) 

    def handle_special(self, special_key):
        def hanler(e):
            func = getattr(self.cur_status, "handle_%s" % special_key, None)
            if func:
                func()
                return "break"
        return hanler

    def handle_keypress(self, e):
        print "keychar is(%s), keycode is (%s)" % (e.char, e.keycode)

        if not self.cur_status.handle_keypress(e.char):
            return "break" #这样就能阻止事件进一步传播



    def set_insert_index(self, index):
        self.t.mark_set("insert", index)

    def add_select_region(self, index1, index2, line_mode = False):
        if self.t.compare(index1, ">", index2):
            index1, index2 = index2, index1
        if line_mode:
            index1 += " linestart"
            index2 += " lineend"
        self.t.tag_add("sel", index1, index2)

    def clear_command_input(self):
        self.c.delete("1.0", "end")

    def hide_command_input(self):
        self.c.grid_forget()

    def show_command_input(self):
        self.c.grid(sticky = tk.E+tk.W)
        self.c.focus_set()

    def get_command_text(self):
        return self.c.get("1.0", "end").encode("utf-8").strip()
    
    def get_select_region(self):
        try: return self.t.get("sel.first", "sel.last")
        except: return ""


    def get_text(self, index1, index2 = None):
        return self.t.get(index1, index2)

    def add_text(self, index, text):
        self.set_cur_status(editor_status.InsertStatus(self, self.t))
        self.t.insert(index, text)
        self.set_cur_status(editor_status.NormalStatus(self, self.t))


    def add_command_text(self, index, text):
        self.c.insert(index, text)

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


        #if self.t.bbox(toindex) is None:
            #if direc == "N":
                #self.t.yview_scroll(-2, tk.UNITS)
            #if direc == "S":
                #self.t.yview_scroll(2, tk.UNITS)
            #if direc == "W":
                #self.t.xview_scroll(-2, tk.UNITS)
            #if direc == "E":
                #self.t.xview_scroll(2, tk.UNITS)
            
        if self.t.bbox(toindex) is None:
            self.t.see(toindex)
    
    def is_lost_vision(self, index):
        return self.t.bbox(index) is None

    def move_vision(self, n, u_type = "lines"):
        self.t.yview_scroll(n, {"lines": tk.UNITS,
                                "pages": tk.PAGES}[u_type])

    def get_insert_index(self):
        return self.t.index("insert")

    def get_index(self, index):
        return self.t.index(index)


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

    def get_win_middle_index(self):
        return "%d.0" % ((int(float(self.get_win_bottom_index())) + 
                    int(float(self.get_win_top_index()))) / 2)


    def set_label(self, info):
        self.l.config(text = info)



if __name__ == "__main__":
    root = tk.Tk()

    editor = GuiEditor(root)
    editor.set_content(edit.Content("./code_demo.py"))
    editor.set_cur_status(editor_status.NormalStatus(editor, editor.t))

    root.mainloop()





