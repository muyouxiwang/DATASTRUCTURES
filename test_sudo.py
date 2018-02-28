# -*- coding=utf-8 -*-


import random
import copy

import Tkinter as tk

class Game(object):
    def __init__(self):
        self.panel = {i:-1 for i in range(1, 82)}

        self.panel_indexs = {i: [] for i in range(1, 82)}

        for ins in self._make_hor_indexs() + \
                   self._make_ver_indexs() + \
                   self._make_rect_indexs():
            for i in ins:
                self.panel_indexs[i].append(ins)

    def _make_hor_indexs(self):
        return [range(i, i + 9) for i in range(1, 82, 9)]

    def _make_ver_indexs(self):
        return [range(i, i + 73, 9) for i in range(1, 10)]

    def _make_rect_indexs(self):
        all = []
        for i in range(1, 82, 27):
            for j in range(i, i + 9, 3):
                ins = []
                for k in range(j, j + 3):
                    ins.extend((k, k + 9, k + 18))
                all.append(ins)
        return all


    def _reset_panel(self):
        self.panel = {i:-1 for i in range(1, 82)}

    def _set_panel(self, panel):
        self.panel = panel

    def _get_all_indexs(self, i):
        return self.panel_indexs[i]



    def _place_num(self, num, i):
        assert(1<=num<=9)
        assert(self.panel[i] == -1)
        ins1, ins2, ins3 = self._get_all_indexs(i)
        for index in ins1 + ins2 + ins3:
            if num == self.panel[index]:
                return False
        self.panel[i] = num
        return True

    def _try_make(self):
        for i in range(1, 82):
            all = range(1, 10)
            num = random.choice(all)
            while not self._place_num(num, i):
                all.remove(num)
                if len(all) == 0:
                    return False
                num = random.choice(all)
        return True

    def make_sudo(self):
        a = self._try_make()
        while not a:
            self._reset_panel()
            a = self._try_make()
        sudo = self._get_panel()
        self._reset_panel()
        return sudo

    def make_puzzle(self, level = 10):
        sudo = self.make_sudo()
        mindexs = random.sample(range(1, 82), level)
        for i in mindexs:
            sudo[i] = -1
        return sudo




    def solve_puzzle(self, puzzle):
        panel = copy.copy(puzzle)

        self._set_panel(panel)
        a = self._try_solve()
        while not a:
            self._set_panel(panel)
            a = self._try_solve()
        answer = self._get_panel()
        self._reset_panel()
        return answer

    def _get_panel(self):
        return copy.copy(self.panel)

    def _try_solve(self):
        for i in range(1, 82):
            if self.panel[i] != -1:
                continue
            all = range(1, 10)
            num = random.choice(all)
            while not self._place_num(num, i):
                all.remove(num)
                if len(all) == 0:
                    return False
                num = random.choice(all)
        return True

    
        
def print_panel(panel = None):
    for i in range(1, 82):
        print panel[i],
        if i%9 == 0:
            print "\n"
    print "=========================\n"
        


class Gui(tk.Frame):
    def __init__(self, root, game):
        tk.Frame.__init__(self, root)
        self.game = game

        f_left = tk.Frame(self)
        f_right = tk.Frame(self)
        

        tk.Button(f_left, text = "问题",
                  command = self.make_puzzle).pack(side = "top")
        self.level = tk.IntVar(value = 10)
        tk.Entry(f_left, textvariable = self.level).pack(side = "top")

        self.text_puzzle = tk.Text(f_left)
        self.text_puzzle.pack(side = "top") 

        tk.Button(f_right, text = "解答",
                  command = self.solve_puzzle).pack(side = "top")
        self.text_answer = tk.Text(f_right)
        self.text_answer.pack(side = "top")

        f_left.pack(side = "left")
        f_right.pack(side = "left")


        self.pack()

    def make_puzzle(self):
        puzzle = self.game.make_puzzle(self.level.get())

        self.text_puzzle.delete("0.0", "end")
        self._show_puzzle(self.text_puzzle, puzzle)

    def solve_puzzle(self):
        puzzle = {i+1:int(n) if n != "-" else -1
                  for i, n in enumerate(
            self.text_puzzle.get("0.0", "end").split())}
        self.text_answer.delete("0.0", "end")
        answer = self.game.solve_puzzle(puzzle)
        self._show_puzzle(self.text_answer, answer)

    def _show_puzzle(self, text, puzzle):
        for i in range(1, 82):
            if puzzle[i] == -1:
                text.insert("end", "-")
            else: 
                text.insert("end", puzzle[i])
            text.insert("end", " ")
            if i%9 == 0:
                text.insert("end",  "\n")
        





def test():
    panel = {i+1:n for i,n in enumerate([3,-1,-1,-1,-1,5,-1,1,-1,
                                         -1,7,-1,-1,-1,6,-1,3,-1,
                                         1,-1,-1,-1,9,-1,-1,-1,-1,
                                         7,-1,8,-1,-1,-1,-1,9,-1,
                                         9,-1,-1,4,-1,8,-1,-1,2,
                                         -1,6,-1,-1,-1,-1,5,-1,1,
                                         -1,-1,-1,-1,4,-1,-1,-1,6,
                                         -1,4,-1,7,-1,-1,-1,2,-1,
                                         -1,2,-1,6,-1,-1,-1,-1,3])}
    g = Game()
    # print_panel(g.solve_puzzle(panel))
    # print_panel(g.solve_puzzle_new(panel))

    g._set_panel(panel)
    print g._can_place_nums(1)
    print g._can_place_nums(2)
    print g._can_place_nums(7)



    
def main():
    root = tk.Tk()
    # screenwidth = root.winfo_screenwidth()
    # screenheight = root.winfo_screenheight()
    # width = 400
    # height = 300
    # size = '%dx%d+%d+%d' % (
    #     width, height, (screenwidth - width)/2, (screenheight - height)/2)
    # root.geometry(size)
    Gui(root, Game()).mainloop()
    
if __name__ == "__main__":
    main()
    # test()


# 1  2  3  4  5  6  7  8  9
# 10 11 12 13 14 15 16 17 18
# 19 20 21 22 23 24 25 26 27
# 28 29 30 31 32 33 34 35 36
# 37 38 39 40 41 42 43 44 45
# 46 47 48 49 50 51 52 53 54
# 55 56 57 58 59 60 61 62 63
# 64 65 66 67 68 69 70 71 72
# 73 74 75 76 77 78 79 80 81

