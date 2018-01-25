# -*- coding=utf-8 -*-

import traceback

import edit
import Tkinter as tk

class EditorStatus(object):
    def __init__(self, editor, text):
        self.editor = editor
        self.t = text
        self.editor.set_label(self.STATUS)
        self.t.focus_set()

        self.key_tmp = ""
        





    def handle_keypress(self, char):
        s = {"/": "slash",
            ":": "colon"}.get(char, char)
        func = getattr(self, "handle_%s" % s, None)
        if func: return func()
        else: self.key_tmp += char

    def handle_escape(self):
        # 清空缓存命令
        self.key_tmp = ""   
        self.editor.remove_all_select_region()
        self.editor.cur_status = NormalStatus(self.editor, self.t)

    def show_some_position(self):
        print "insert point(%s)" % self.t.get("insert")
        print "selected text---%s---" % self.t.get("sel.first", "sel.last")


class NormalStatus(EditorStatus):
    STATUS = "普通模式"

    def __init__(self, editor, text):
        super(NormalStatus, self).__init__(editor, text)

        self.t.config(state = "disabled")

        self.editor.add_highlight("insert", "insert + 1c")

        self.multi_key_map = {"gg": self.go_to_begin}


    def handle_keypress(self, char):
        self.key_tmp += char
        if len(self.key_tmp) >= 3:
            self.key_tmp = ""
        func = self.multi_key_map.get(self.key_tmp)
        if func:
            self.key_tmp = ""
            return func()
        return super(NormalStatus, self).handle_keypress(char)

    def go_to_begin(self):

        self.editor.move_visual_cursor("1.0", "N")

        self.editor.focus_index("insert")
        print self.t.get("insert", "insert + 1c")

    def handle_H(self):
        win_top_index = self.editor.get_win_top_index()
        self.editor.move_visual_cursor(win_top_index, "N")

    def handle_L(self):
        win_bottom_index = self.editor.get_win_bottom_index()
        self.editor.move_visual_cursor(win_bottom_index, "S")

    def handle_M(self):
        win_top_index = self.editor.get_win_top_index()
        win_bottom_index = self.editor.get_win_bottom_index()
        win_mid_index = "%d.0" % ((int(float(win_bottom_index)) + 
                                int(float(win_top_index))) / 2)
        self.editor.move_visual_cursor(win_mid_index)

    def handle_G(self):
        self.editor.move_visual_cursor("end", "S")

        self.editor.focus_index("insert")
        print self.t.get("insert", "insert + 1c")

    def handle_slash(self):
        self.editor.cur_status = CommandStatus(self.editor, self.t, "search")
        return "break"

    def handle_colon(self):
        self.editor.cur_status = CommandStatus(self.editor, self.t, "command")
        return "break"


    def handle_j(self):
        self.editor.move_visual_cursor("insert + 1 lines", "S")
        print self.t.get("insert", "insert + 1c")

    def handle_l(self):
        self.editor.move_visual_cursor("insert + 1c", "E")
        print self.t.get("insert", "insert + 1c")

    def handle_k(self):
        self.editor.move_visual_cursor("insert - 1 lines", "N")
        print self.t.get("insert", "insert + 1c")

    def handle_h(self):
        self.editor.move_visual_cursor("insert - 1c", "W")
        print self.t.get("insert", "insert + 1c")

    def handle_i(self):
        self.editor.cur_status = InsertStatus(self.editor, self.t)
        return "break"  #这样就能阻止事件进一步传播

    def handle_v(self):
        self.editor.cur_status = VisualStatus(self.editor, self.t, False)
        return "break"

    def handle_V(self):
        self.editor.cur_status = VisualStatus(self.editor, self.t, True)
        return "break"

    def handle_p(self):
        self.editor.cur_status = InsertStatus(self.editor, self.t)
        if self.editor.clipboard:
            index = self.editor.get_insert_index()
            self.editor.add_text(index, self.editor.clipboard)
        self.handle_escape()


class InsertStatus(EditorStatus):
    STATUS = "插入模式"
    def __init__(self, editor, text):
        super(InsertStatus, self).__init__(editor, text)

        self.t.config(state = "normal")
        self.editor.remove_highlight("insert")
        self.just_in = True


        self.multi_key_map = {}




class VisualStatus(EditorStatus):
    STATUS = "可视模式 "
    def __init__(self, editor, text, line_mode = False):
        super(VisualStatus, self).__init__(editor, text)

        self.line_mode = line_mode

        self.t.config(state = "disabled")
        self.multi_key_map = {}


        
        if self.line_mode:
            self.editor.move_visual_cursor("insert linestart")
        self.start_index = self.editor.get_insert_index()



    def handle_j(self):
        self.editor.move_visual_cursor("insert + 1 lines", "S")
    
        self.editor.remove_all_select_region()
        self.editor.add_select_region(self.start_index, "insert", self.line_mode)



    def handle_l(self):
        if self.line_mode:
            return
        self.editor.move_visual_cursor("insert + 1c", "E")
        self.editor.remove_all_select_region()
        self.editor.add_select_region(self.start_index, "insert")

    def handle_k(self):
        self.editor.move_visual_cursor("insert - 1 lines", "N")
        self.editor.remove_all_select_region()

        self.editor.add_select_region(self.start_index, "insert", self.line_mode)

    def handle_h(self):
        if self.line_mode:
            return
        self.editor.move_visual_cursor("insert - 1c", "W")
        self.editor.remove_all_select_region()
        self.editor.add_select_region(self.start_index, "insert")

    def handle_y(self):
        text = self.editor.get_select_region()
        print "the select is +++%s+++" % text
        if text:
            self.editor.clipboard = text
        self.handle_escape()



class CommandStatus(EditorStatus):
    STATUS = "命令模式 "
    def __init__(self, editor, text, cmd_type):
        super(CommandStatus, self).__init__(editor, text)
    
        self.cmd_type = cmd_type

        self.c = self.editor.c
        self.v = self.editor.v


        self.editor.remove_highlight("insert")
        self.show_command_input()
        self.c.bind("<Return>", self.input_finish)
        self.c.bind("<KeyRelease>", self.do_search)

        self.highs = set()

    def back_to_normal(self):
        self.v.set("")
        #self.c.pack_forget()
        self.c.grid_forget()
        self.handle_escape()

    def show_command_input(self):
        self.v.set({"search": "/", "command": ":"}[self.cmd_type])
        self.c.icursor("end")
        self.c.grid()
        
        self.c.focus_set()


    def input_finish(self, e):
        if self.cmd_type == "command":
            self.do_command()
        self.back_to_normal()

    def do_command(self):
        #cmd = self.v.get().encode("utf-8")[1:]
        #if cmd:
            #print "do command(%s)" % cmd
        try:
            print eval(self.v.get()[1:])
        except:
            print traceback.format_exc()
        self.v.set("")


    def do_search(self, e):
        if len(self.v.get()) == 0:
            self.back_to_normal()

        if self.cmd_type == "command":
            return

        
        s = self.v.get().encode("utf-8")[1:]
        searched = edit.search(s)
        for item in self.highs:
            if item not in searched:
                self.t.tag_remove("highlight",
                item[0], item[1])

        self.highs.clear()
        for i, j in searched:
            x = "%d.%d" % (i+1, j),
            y ="%d.%d" % (i+1, j + len(s.decode("utf-8")))
            self.editor.add_highlight(x, y)
            self.highs.add((x, y))


  # 正常模式 (Normal-mode) 
  # 插入模式 (Insert-mode)
  # 命令模式 (Command-mode)
  # 可视模式 (Visual-mode)


