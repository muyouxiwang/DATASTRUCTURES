# -*- coding=utf-8 -*-






panel = {i:-1 for i in range(1, 82)}


def reset_panel():
    panel = {i:-1 for i in range(1, 82)}


panel_indexs = {i: [0,0,0] for i in range(1, 82)}

tmp = [1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in tmp:
    panel_indexs[i][0] = tmp

tmp = [10,11, 12,13, 14,15, 16,17, 18]
for i in tmp:
    panel_indexs[i][0] = tmp

tmp = [19,20, 21,22, 23,24, 25,26, 27]
for i in tmp:
    panel_indexs[i][0] = tmp

tmp = [28,29, 30,31, 32,33, 34,35, 36]
for i in tmp:
    panel_indexs[i][0] = tmp

tmp = [37,38, 39,40, 41,42, 43,44, 45]
for i in tmp:
    panel_indexs[i][0] = tmp

tmp = [46,47, 48,49, 50,51, 52,53, 54]
for i in tmp:
    panel_indexs[i][0] = tmp

tmp = [55,56, 57,58, 59,60, 61,62, 63]
for i in tmp:
    panel_indexs[i][0] = tmp

tmp = [64,65, 66,67, 68,69, 70,71, 72]
for i in tmp:
    panel_indexs[i][0] = tmp

tmp = [73,74, 75,76, 77,78, 79,80, 81]
for i in tmp:
    panel_indexs[i][0] = tmp











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


tmp = [1, 10, 19, 28, 37, 46, 55, 64, 73]
for i in tmp:
    panel_indexs[i][1] = tmp
tmp = [2, 11, 20, 29, 38, 47, 56, 65, 74]
for i in tmp:
    panel_indexs[i][1] = tmp
tmp = [3, 12, 21, 30, 39, 48, 57, 66, 75]
for i in tmp:
    panel_indexs[i][1] = tmp
tmp = [4, 13, 22, 31, 40, 49, 58, 67, 76]
for i in tmp:
    panel_indexs[i][1] = tmp
tmp = [5, 14, 23, 32, 41, 50, 59, 68, 77]
for i in tmp:
    panel_indexs[i][1] = tmp
tmp = [6, 15, 24, 33, 42, 51, 60, 69, 78]
for i in tmp:
    panel_indexs[i][1] = tmp
tmp = [7, 16, 25, 34, 43, 52, 61, 70, 79]
for i in tmp:
    panel_indexs[i][1] = tmp
tmp = [8, 17, 26, 35, 44, 53, 62, 71, 80]
for i in tmp:
    panel_indexs[i][1] = tmp
tmp = [9, 18, 27, 36, 45, 54, 63, 72, 81]
for i in tmp:
    panel_indexs[i][1] = tmp

tmp = [1,   2,   3, 10,   11,   12, 19,   20,   21]    
for i in tmp:
    panel_indexs[i][2] = tmp

tmp = [4,   5,   6, 13,   14,   15, 22,   23,   24]
for i in tmp:
    panel_indexs[i][2] = tmp
    
tmp = [7,   8,   9, 16,   17,   18, 25,   26,   27]    
for i in tmp:
    panel_indexs[i][2] = tmp
    
tmp = [28,   29,   30, 37,38,39,46,47,48]
for i in tmp:
    panel_indexs[i][2] = tmp
    
tmp = [31,   32,   33, 40,41,42,49,50,51]    
for i in tmp:
    panel_indexs[i][2] = tmp
    
tmp = [34,   35,   36, 43,44,45,52,53,54]    
for i in tmp:
    panel_indexs[i][2] = tmp
    
tmp = [55,   56,   57, 64,   65,   66, 73,   74,   75]   
for i in tmp:
    panel_indexs[i][2] = tmp
    
tmp = [58,   59,   60, 67,   68,   69, 76,   77,   78]
for i in tmp:
    panel_indexs[i][2] = tmp
    
tmp = [61,   62,   63, 70,   71,   72, 79,   80,   81]
for i in tmp:
    panel_indexs[i][2] = tmp
    

def get_all_indexs(i):
    return panel_indexs[i]




def is_legel(num, i):
    assert(1<=num<=9)
    assert(panel[i] == -1)
    is1, is2, is3 = get_all_indexs(i)
    for index in is1:
        if num == panel[index]:
            return False
    for index in is2:
        if num == panel[index]:
            return False
    for index in is3:
        if num == panel[index]:
            return False
    panel[i] = num
    return True



def print_panel():
    for i in range(1, 82):
        print panel[i],
        if i%9 == 0:
            print "\n"


import random

def make_answer():
    for i in range(1, 82):
        all = range(1, 10)
        num = random.choice(all)
        while not is_legel(num, i):
            all.remove(num)
            if len(all) == 0:
                return False
            num = random.choice(all)
    return True

for _ in range(3):
    a = make_answer()
    while not a:
        a = make_answer()
    print_panel()
    reset_panel()
        
        

    
    
    

