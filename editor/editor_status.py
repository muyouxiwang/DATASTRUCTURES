# -*- coding=utf-8 -*-

import traceback

import Tkinter as tk

class EditorStatus(object):
    def __init__(self, editor, text):
        self.editor = editor
        self.t = text
        self.t.focus_set()

        self.key_tmp = ""

        self.digit_prefix = ""
        


    def handle_keypress(self, char):
        try:
            x = int(char)
            if 0 <= x <= 9:
                self.digit_prefix += char
                self.key_tmp = ""
                return
        except: pass

        s = {"/": "slash",
            ":": "colon",
            "^": "upco",
            "$": "dollar",
            "%": "percent"}.get(char, char)
        func = getattr(self, "handle_%s" % s, None)
        if func and not self.key_tmp: 
            for _ in range(int(self.digit_prefix) if self.digit_prefix else 1):
                func()
            self.digit_prefix = ""
            self.key_tmp = ""
            return
        else:
            self.key_tmp += char
            if len(self.key_tmp) == 2:
                func = self.multi_key_map.get(self.key_tmp)
                if func:
                    for _ in range(int(self.digit_prefix) if self.digit_prefix else 1):
                        stop = func()
                        if stop:
                            break
                self.digit_prefix = ""
                self.key_tmp = ""

    def handle_escape(self):
        # 清空缓存命令
        self.key_tmp = ""   
        self.digit_prefix = ""

        self.editor.remove_all_select_region()
        self.editor.set_cur_status(NormalStatus(self.editor, self.t)) 

    def show_some_position(self):
        print "insert point(%s)" % self.t.get("insert")
        print "selected text---%s---" % self.t.get("sel.first", "sel.last")

class NormalStatus(EditorStatus):
    STATUS = "普通模式"

    def __init__(self, editor, text):
        super(NormalStatus, self).__init__(editor, text)

        self.t.config(state = "disabled")

        self.editor.add_highlight("insert", "insert + 1c")

        self.multi_key_map = {"gg": self.go_to_begin,
                                "zz": self.middle_the_insert,
                                "zj": self.see_next_page,
                                "zk": self.see_last_page}

    def go_to_begin(self):

        self.editor.move_visual_cursor("1.0", "N")

        self.editor.focus_index("insert")
        print self.t.get("insert", "insert + 1c")

    def middle_the_insert(self):
        insert_line = int(float(self.editor.get_insert_index()))
        mid_line = int(float(self.editor.get_win_middle_index()))


        move_line_num = insert_line - mid_line
        if move_line_num != 0:
            print "i need to move %d line(%d, %d)" % (move_line_num, insert_line, mid_line)
            self.editor.move_vision(move_line_num)
    
    def see_next_page(self):
        bottom_index = self.editor.get_win_bottom_index()
        self.editor.move_vision(1, "pages")
        self.editor.move_visual_cursor(bottom_index)
            
 

    def see_last_page(self):
        top_index = self.editor.get_win_top_index()
        self.editor.move_vision(-1, "pages")
        self.editor.move_visual_cursor(top_index)

    def handle_H(self):
        win_top_index = self.editor.get_win_top_index()
        self.editor.move_visual_cursor(win_top_index, "N")

    def handle_L(self):
        win_bottom_index = self.editor.get_win_bottom_index()
        self.editor.move_visual_cursor(win_bottom_index, "S")

    def handle_M(self):
        win_mid_index = self.editor.get_win_middle_index()
        self.editor.move_visual_cursor(win_mid_index)

    def handle_G(self):
        if self.digit_prefix:
            cur_line = int(float(self.editor.get_index("insert")))
            go_line = int(self.digit_prefix)
            dire = "S" if cur_line < go_line else "N"
            self.editor.move_visual_cursor("%d.0" % go_line, dire) 
            self.editor.focus_index("insert")
            return "stop"

        self.editor.move_visual_cursor("end", "S")
        self.editor.focus_index("insert")

    def handle_slash(self):
        self.editor.set_cur_status(CommandStatus(self.editor, self.t, "search")) 
        return

    def handle_colon(self):
        self.editor.set_cur_status(CommandStatus(self.editor, self.t, "command"))  
        return

    def handle_upco(self):
        self.editor.move_visual_cursor("insert linestart")

    def handle_dollar(self):
        self.editor.move_visual_cursor("insert lineend")

    def handle_percent(self):
        board = [("(", ")"), ("[", "]"), 
            ("{", "}"), ('"', '"'), ("'", "'")]
        min_distance = -1
        min_first = -1
        min_last = -1
        insert_index = self.editor.get_insert_index()
        for cc in board:
            index = insert_index.split(".")
            x1, y1, x2, y2 = self.editor.content.get_close_char(
                        int(index[0])-1, int(index[1]), cc[0],
                        cc[1])
            if x1 == -1:
                continue
            first = "%d.%d" % (x1+1, y1)
            last = "%d.%d" % (x2+1, y2)
            #first += " - 1c"
            #last += " + 1c"
            first = self.editor.get_index(first)
            last = self.editor.get_index(last)

            distance = float(insert_index) - float(first)
            if min_distance == -1:
                min_distance = distance
                min_first = first
                min_last = last
            else:
                if distance < min_distance:
                    min_distance = distance
                    min_first = first
                    min_last = last
        if min_first == -1:
            return
        if min_first == insert_index:
            self.editor.move_visual_cursor(min_last)
        else:
            self.editor.move_visual_cursor(min_first)

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
        self.editor.set_cur_status(InsertStatus(self.editor, self.t)) 
        return 

    def handle_v(self):
        self.editor.set_cur_status(VisualStatus(self.editor, self.t, False)) 
        return

    def handle_V(self):
        self.editor.set_cur_status(VisualStatus(self.editor, self.t, True)) 
        return

    def handle_p(self):
        if self.editor.clipboard:
            index = self.editor.get_insert_index()
            self.editor.add_text(index, self.editor.clipboard)

    def handle_c_e(self):
        self.editor.move_vision(1)
        if self.editor.is_lost_vision("insert"):
            self.editor.move_visual_cursor("insert - 1 lines", "N")
    
    def handle_c_y(self):
        self.editor.move_vision(-1)
        if self.editor.is_lost_vision("insert"):
            self.editor.move_visual_cursor("insert + 1 lines", "S")

    def handle_u(self):
        self.editor.undo()

    def handle_c_r(self):
        self.editor.redo()

    def handle_w(self):
        index = self.editor.get_insert_index().split(".")
        x, y = self.editor.content.get_next_word(int(index[0]) - 1,
                                    int(index[1]))
        self.editor.move_visual_cursor("%d.%d" % (x + 1,
                                                y + 1))
    
    def handle_e(self):
        index = self.editor.get_insert_index().split(".")
        x, y = self.editor.content.get_word_end(int(index[0]) - 1,
                                    int(index[1]))
        self.editor.move_visual_cursor("%d.%d" % (x + 1,
                                                y))
        
    def handle_b(self):
        index = self.editor.get_insert_index().split(".")
        x, y = self.editor.content.get_word_start(int(index[0]) - 1,
                                    int(index[1]))
        self.editor.move_visual_cursor("%d.%d" % (x + 1, y))
        



class InsertStatus(EditorStatus):
    STATUS = "插入模式"
    def __init__(self, editor, text):
        super(InsertStatus, self).__init__(editor, text)

        self.t.config(state = "normal")
        self.editor.remove_highlight("insert")
        self.just_in = True


        self.multi_key_map = {}

    def handle_keypress(self, char):
        return True



class VisualStatus(NormalStatus):
    STATUS = "可视模式 "
    def __init__(self, editor, text, line_mode = False):
        super(VisualStatus, self).__init__(editor, text)

        self.line_mode = line_mode

        self.t.config(state = "disabled")

        self.multi_key_map = \
        {
        "i(" : self.select_close_char("(", ")"),
        "i)" : self.select_close_char("(", ")"),
        "i[" : self.select_close_char("[", "]"),
        "i]" : self.select_close_char("[", "]"),
        "i{" : self.select_close_char("{", "}"),
        "i}" : self.select_close_char("{", "}"),
        'i"' : self.select_close_char('"', '"'),
        "i'" : self.select_close_char("'", "'"),
        "a(" : self.select_close_char("(", ")", False),
        "a)" : self.select_close_char("(", ")", False),
        "a[" : self.select_close_char("[", "]", False),
        "a]" : self.select_close_char("[", "]", False),
        "a{" : self.select_close_char("{", "}", False),
        "a}" : self.select_close_char("{", "}", False),
        'a"' : self.select_close_char('"', '"', False),
        "a'" : self.select_close_char("'", "'", False)
        }

#方括号
#brackets
#圆括号
#parentheses
#花括号
#Curly_braces     
#单引号
#single_quotes
#双引号
#double_quotes


        if self.line_mode:
            self.editor.move_visual_cursor("insert linestart")
        self.start_index = self.editor.get_insert_index()


        self.handle_i = None
        self.handle_a = None


    def select_close_char(self, start_c, end_c, inside = True):
        def _():
            index = self.editor.get_insert_index().split(".")
            x1, y1, x2, y2 = self.editor.content.get_close_char(
                        int(index[0])-1, int(index[1]), start_c,
                        end_c)
            if -1 == x1:
                return

            sel_first = "%d.%d" % (x1+1, y1)
            sel_last = "%d.%d" % (x2+1, y2)
            if inside:
                sel_first += " + 1c"
            else:
                #sel_first += " - 1c"
                sel_last += " + 1c"
                pass

            self.start_index = self.editor.get_index(sel_first)
            self.editor.add_select_region(self.start_index,
                                            sel_last)
            self.editor.move_visual_cursor("sel.last")
        return _

    def select_in_brackets(self):
        pass
    def select_in_curly_braces(self):
        pass
    def select_in_double_quotes(self):
        pass
    def select_in_single_quotes(self):
        pass
    def select_out_parentheses(self):
        pass
    def select_out_brackets(self):
        pass
    def select_out_curly_braces(self):
        pass
    def select_out_double_quotes(self):
        pass
    def select_out_single_quotes(self):
        pass


    def _add_select_region(self):
        self.editor.remove_all_select_region()
        self.editor.add_select_region(self.start_index, "insert", self.line_mode)
        

    def handle_j(self):
        super(VisualStatus, self).handle_j()
        self._add_select_region()
    

    def handle_l(self):
        if self.line_mode:
            return
        super(VisualStatus, self).handle_l()
        self._add_select_region()

    def handle_k(self):
        super(VisualStatus, self).handle_k()
        self._add_select_region()


    def handle_h(self):
        if self.line_mode:
            return
        super(VisualStatus, self).handle_h()
        self._add_select_region()

    def handle_w(self):
        super(VisualStatus, self).handle_w()
        self._add_select_region()

    def handle_e(self):
        super(VisualStatus, self).handle_e()
        self._add_select_region()

    def handle_b(self):
        super(VisualStatus, self).handle_b()
        self._add_select_region()
        

    def handle_upco(self):
        super(VisualStatus, self).handle_upco()
        self._add_select_region()

    def handle_dollar(self):
        super(VisualStatus, self).handle_dollar()
        self._add_select_region()

    def handle_y(self):
        text = self.editor.get_select_region()
        print "the select is +++%s+++" % text
        if text:
            self.editor.clipboard = text
        self.handle_escape()

    def handle_o(self):
        if self.editor.get_select_region():
            if self.editor.get_index("insert") ==\
                self.editor.get_index("sel.first"):
                self.editor.move_visual_cursor("sel.last")
            else:
                self.editor.move_visual_cursor("sel.first")

                
        



class CommandStatus(EditorStatus):
    STATUS = "命令模式 "
    def __init__(self, editor, text, cmd_type):
        super(CommandStatus, self).__init__(editor, text)
    
        self.cmd_type = cmd_type

        self.editor.remove_highlight("insert")
        self.show_command_input()

        self.highs = set()

    def handle_keypress(self, char):
        return True

    def back_to_normal(self):
        self.editor.clear_command_input()
        self.editor.hide_command_input()
        self.handle_escape()

    def show_command_input(self):
        self.editor.add_command_text("1.0", {"search": "/", "command": ":"}[self.cmd_type])
        self.editor.show_command_input()


    def handle_return(self):
        if self.cmd_type == "command":
            self.do_command()
        self.back_to_normal()
        return

    def do_command(self):
        cmd = self.editor.get_command_text()[1:]

        if cmd == "q":
            self.editor.quit()

        if cmd.startswith("e "):
            filepath = cmd[2:].strip()
            self.editor.open_new_file(filepath)

        # try:
        #     print eval(cmd)
        # except:
        #     print traceback.format_exc()

        self.editor.clear_command_input()


    def handle_release(self):
        text = self.editor.get_command_text()
        if not text:
            self.back_to_normal()
            return

        if self.cmd_type == "command":
            return

        p = text[1:]
        if not p:
            return
        searched = self.editor.content.search(p)
        for item in self.highs:
            if item not in searched:
                self.editor.remove_highlight(item[0], item[1])

        self.highs.clear()
        for i, j in searched:
            x = "%d.%d" % (i+1, j),
            y = "%d.%d" % (i+1, j + len(p.decode("utf-8")))
            self.editor.add_highlight(x, y)
            self.highs.add((x, y))

    def handle_tab(self):
        pass

  # 正常模式 (Normal-mode) 
  # 插入模式 (Insert-mode)
  # 命令模式 (Command-mode)
  # 可视模式 (Visual-mode)


  
