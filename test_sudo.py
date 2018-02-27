# -*- coding=utf-8 -*-


import random
import copy

import Tkinter as tk

class Game(object):
    def __init__(self):
        self.panel = {i:-1 for i in range(1, 82)}

        self.panel_indexs = {i: [0,0,0] for i in range(1, 82)}

        tmp = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in tmp:
            self.panel_indexs[i][0] = tmp

        tmp = [10,11, 12,13, 14,15, 16,17, 18]
        for i in tmp:
            self.panel_indexs[i][0] = tmp

        tmp = [19,20, 21,22, 23,24, 25,26, 27]
        for i in tmp:
            self.panel_indexs[i][0] = tmp

        tmp = [28,29, 30,31, 32,33, 34,35, 36]
        for i in tmp:
            self.panel_indexs[i][0] = tmp

        tmp = [37,38, 39,40, 41,42, 43,44, 45]
        for i in tmp:
            self.panel_indexs[i][0] = tmp

        tmp = [46,47, 48,49, 50,51, 52,53, 54]
        for i in tmp:
            self.panel_indexs[i][0] = tmp

        tmp = [55,56, 57,58, 59,60, 61,62, 63]
        for i in tmp:
            self.panel_indexs[i][0] = tmp

        tmp = [64,65, 66,67, 68,69, 70,71, 72]
        for i in tmp:
            self.panel_indexs[i][0] = tmp

        tmp = [73,74, 75,76, 77,78, 79,80, 81]
        for i in tmp:
            self.panel_indexs[i][0] = tmp

        tmp = [1, 10, 19, 28, 37, 46, 55, 64, 73]
        for i in tmp:
            self.panel_indexs[i][1] = tmp
        tmp = [2, 11, 20, 29, 38, 47, 56, 65, 74]
        for i in tmp:
            self.panel_indexs[i][1] = tmp
        tmp = [3, 12, 21, 30, 39, 48, 57, 66, 75]
        for i in tmp:
            self.panel_indexs[i][1] = tmp
        tmp = [4, 13, 22, 31, 40, 49, 58, 67, 76]
        for i in tmp:
            self.panel_indexs[i][1] = tmp
        tmp = [5, 14, 23, 32, 41, 50, 59, 68, 77]
        for i in tmp:
            self.panel_indexs[i][1] = tmp
        tmp = [6, 15, 24, 33, 42, 51, 60, 69, 78]
        for i in tmp:
            self.panel_indexs[i][1] = tmp
        tmp = [7, 16, 25, 34, 43, 52, 61, 70, 79]
        for i in tmp:
            self.panel_indexs[i][1] = tmp
        tmp = [8, 17, 26, 35, 44, 53, 62, 71, 80]
        for i in tmp:
            self.panel_indexs[i][1] = tmp
        tmp = [9, 18, 27, 36, 45, 54, 63, 72, 81]
        for i in tmp:
            self.panel_indexs[i][1] = tmp

        tmp = [1,   2,   3, 10,   11,   12, 19,   20,   21]    
        for i in tmp:
            self.panel_indexs[i][2] = tmp

        tmp = [4,   5,   6, 13,   14,   15, 22,   23,   24]
        for i in tmp:
            self.panel_indexs[i][2] = tmp

        tmp = [7,   8,   9, 16,   17,   18, 25,   26,   27]    
        for i in tmp:
            self.panel_indexs[i][2] = tmp

        tmp = [28,   29,   30, 37,38,39,46,47,48]
        for i in tmp:
            self.panel_indexs[i][2] = tmp

        tmp = [31,   32,   33, 40,41,42,49,50,51]    
        for i in tmp:
            self.panel_indexs[i][2] = tmp

        tmp = [34,   35,   36, 43,44,45,52,53,54]    
        for i in tmp:
            self.panel_indexs[i][2] = tmp

        tmp = [55,   56,   57, 64,   65,   66, 73,   74,   75]   
        for i in tmp:
            self.panel_indexs[i][2] = tmp

        tmp = [58,   59,   60, 67,   68,   69, 76,   77,   78]
        for i in tmp:
            self.panel_indexs[i][2] = tmp

        tmp = [61,   62,   63, 70,   71,   72, 79,   80,   81]
        for i in tmp:
            self.panel_indexs[i][2] = tmp

    def _reset_panel(self):
        self.panel = {i:-1 for i in range(1, 82)}

    def _set_panel(self, panel):
        self.panel = panel

    def _get_all_indexs(self, i):
        return self.panel_indexs[i]


    def _place_num(self, num, i):
        assert(1<=num<=9)
        assert(self.panel[i] == -1)
        is1, is2, is3 = self._get_all_indexs(i)
        for index in is1 + is2 + is3:
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
        self.puzzle = self.game.make_puzzle()

        self.text_puzzle.delete("0.0", "end")
        for i in range(1, 82):
            if self.puzzle[i] == -1:
                self.text_puzzle.insert("end", "*")
            else: 
                self.text_puzzle.insert("end", self.puzzle[i])
            self.text_puzzle.insert("end", " ")
            if i%9 == 0:
                self.text_puzzle.insert("end",  "\n")

    def solve_puzzle(self):
        self.text_answer.delete("0.0", "end")
        answer = self.game.solve_puzzle(self.puzzle)
        for i in range(1, 82):
            self.text_answer.insert("end", answer[i])
            self.text_answer.insert("end", " ")
            if i%9 == 0:
                self.text_answer.insert("end",  "\n")


    
def main():
    Gui(tk.Tk(), Game()).mainloop()
    
main()
        #1  2  3  4  5  6  7  8  9

        #10 11 12 13 14 15 16 17 18

        #19 20 21 22 23 24 25 26 27

        #28 29 30 31 32 33 34 35 36

        #37 38 39 40 41 42 43 44 45

        #46 47 48 49 50 51 52 53 54

        #55 56 57 58 59 60 61 62 63

        #64 65 66 67 68 69 70 71 72

        #73 74 75 76 77 78 79 80 81

        #with open("tmp.txt", "w") as wf:

            #for i in range(1, 81):
                #print >> wf, i, " ", i+1, " ", i+2
                #print >> wf, i+9, " ", i+1+9, " ", i+2+9
                #print >> wf, i+9+9, " ", i+1+9+9, " ", i+2+9+9
    
