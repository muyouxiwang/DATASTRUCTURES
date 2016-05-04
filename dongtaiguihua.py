# -*- coding=utf-8 -*-

import functools

def mywrap(f):
    cache = {}
    @functools.wraps(f)
    def wrap(*arg):
        if arg not in cache:
            cache[arg] = f(*arg)
        return cache[arg]
    return wrap

def mywrap2(f):
    cache = {}
    @functools.wraps(f)
    def wrap(*arg):
        if arg in cache:
            print "%s, %s" % arg
            return cache[arg]
        cache[arg] = f(*arg)
        return cache[arg]
    return wrap

gold_mine = [500, 108, 683, 111, 98, 10, 837, 973, 1234, 555]
mine_man = [100, 20, 79, 30, 48, 66, 101, 200, 99, 10]

#gold_mine = [6, 6, 9]
#mine_man = [3, 3, 5]

@mywrap
def dongtaiguihua(mannum, n):
    if 0 == n:
        if mannum >= mine_man[0]:
            return gold_mine[0]
        else:
            return 0
    else:
        if mannum >= mine_man[n]:
            x1 = dongtaiguihua(mannum - mine_man[n], n - 1) + gold_mine[n]
            x2 = dongtaiguihua(mannum, n - 1)
            return max(x1, x2)
        else:
            return dongtaiguihua(mannum, n - 1)




def main():
    while 1:
        mannum = int(raw_input("input man num:"))
        if mannum == 0:
            break
        print dongtaiguihua(mannum, len(gold_mine) - 1)




if __name__ == "__main__":
    main()
