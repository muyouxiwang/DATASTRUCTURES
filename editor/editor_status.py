# -*- coding=utf-8 -*-

import edit

class EditorStatus(object):
    def __init__(self, editor, text):
        self.editor = editor
        self.t = text
        self.editor.set_label(self.STATUS)
        self.t.focus_set()

        self.key_tmp = ""


        self.t.bind("<KeyPress>", self.handle_keypress)
        self.t.bind("<Escape>", self.back_to_normal)

    def handle_keypress(self, e):
        print "keychar is(%s), keycode is (%s)" % (e.char, e.keycode)

        if self.STATUS == "普通模式" and self.key_tmp:
            self.key_tmp += e.char
            if len(self.key_tmp) >= 3:
                self.key_tmp = ""
            func = self.multi_key_map.get(self.key_tmp)
            if func:
                self.key_tmp = ""
                return func()
        else:
            s = {"/": "slash",
                ":": "colon"}.get(e.char, e.char)
            func = getattr(self, "handle_%s" % s, None)
            if func: return func()
            else: self.key_tmp += e.char

    def back_to_normal(self, e):
        # 清空缓存命令
        self.key_tmp = ""   
        # 去掉v模式下的高亮选择，没有选中的情况下会报错，所以用try
        try: self.t.tag_remove("sel", "sel.first", "sel.last")
        except: pass
        self.editor.cur_status = NormalStatus(self.editor, self.t)

        return "break"

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


    def go_to_begin(self):

        self.editor.move_visual_cursor("1.0")

        self.editor.focus_index("insert")
        print self.t.get("insert", "insert + 1c")

    def handle_G(self):
        self.editor.move_visual_cursor("end")

        self.editor.focus_index("insert")
        print self.t.get("insert", "insert + 1c")

    def handle_slash(self):
        self.editor.cur_status = CommandStatus(self.editor, self.t, "search")
        return "break"

    def handle_colon(self):
        self.editor.cur_status = CommandStatus(self.editor, self.t, "command")
        return "break"


    def handle_j(self):
        self.editor.move_visual_cursor("insert + 1 lines")
        print self.t.get("insert", "insert + 1c")

    def handle_l(self):
        self.editor.move_visual_cursor("insert + 1c")
        print self.t.get("insert", "insert + 1c")

    def handle_k(self):
        self.editor.move_visual_cursor("insert - 1 lines")
        print self.t.get("insert", "insert + 1c")

    def handle_h(self):
        self.editor.move_visual_cursor("insert - 1c")
        print self.t.get("insert", "insert + 1c")

    def handle_i(self):
        self.editor.cur_status = InsertStatus(self.editor, self.t)
        return "break"  #这样就能阻止事件进一步传播

    def handle_v(self):
        self.editor.cur_status = VisualStatus(self.editor, self.t)
        return "break"




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
    def __init__(self, editor, text):
        super(VisualStatus, self).__init__(editor, text)

        self.key_tmp = ""
        self.t.config(state = "disabled")
        self.editor.add_highlight("insert", "insert + 1c")

        self.t.mark_set("v_first", "insert")
    
        self.multi_key_map = {}



    def handle_j(self):
        self.editor.remove_highlight("insert")
        self.t.tag_remove("sel", "v_first", "insert")
        self.editor.add_select_region("insert", "insert + 1 lines")
        self.editor.set_insert_index("insert + 1 lines")
        self.editor.add_highlight("insert")

        self.show_some_position()


    def handle_l(self):
        self.editor.remove_highlight("insert")
        self.editor.add_select_region("insert", "insert + 1c")
        self.editor.set_insert_index("insert + 1c")
        self.editor.add_highlight("insert")

        self.show_some_position()

    def handle_k(self):
        self.editor.remove_highlight("insert")
        self.editor.add_select_region("insert", "insert - 1 lines")
        self.editor.set_insert_index("insert - 1 lines")
        self.editor.add_highlight("insert")

        self.show_some_position()

    def handle_h(self):
        self.editor.remove_highlight("insert")
        self.editor.add_select_region("insert", "insert - 1c")
        self.editor.set_insert_index("insert - 1c")
        self.editor.add_highlight("insert")

        self.show_some_position()

class CommandStatus(EditorStatus):
    STATUS = "命令模式 "
    def __init__(self, editor, text, cmd_type):
        super(CommandStatus, self).__init__(editor, text)
    
        self.cmd_type = cmd_type

        self.c = self.editor.c
        self.v = self.editor.v

        self.show_command_input()
        self.c.bind("<Return>", self.input_finish)
        self.c.bind("<KeyRelease>", self.do_search)

        self.highs = set()

    def back_to_normal(self):
        self.v.set("")
        self.c.pack_forget()
        super(CommandStatus, self).back_to_normal(None)

    def show_command_input(self):
        self.v.set({"search": "/", "command": ":"}[self.cmd_type])
        self.c.icursor("end")
        self.c.pack()
        
        self.c.focus_set()


    def input_finish(self, e):
        if self.cmd_type == "command":
            self.do_command()
        self.back_to_normal()

    def do_command(self):
        cmd = self.v.get().encode("utf-8")[1:]
        if cmd:
            print "do command(%s)" % cmd

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


