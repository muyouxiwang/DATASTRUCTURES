# -*- coding=utf-8 -*-

import random


def naive_max_perm(M, A=None): 
    if A is None:                                            # The elt. set not supplied? 
        A = set(range(len(M)))                              # A = {0, 1, ... , n-1}  
    if len(A) == 1: return A                                 # Base case -- single-elt. A 
    B = set(M[i] for i in A)                                 # The "pointed to" elements 
    C = A - B                                                # "Not pointed to" elements 
    if C:                                                    # Any useless elements? 
        A.remove(C.pop())                                   # Remove one of them  
        return naive_max_perm(M, A)                         # Solve remaining problem 
    return A   



def my_naive_max_perm(M):
    happy = set()
    seated = set()
    for index, man_wish in enumerate(M):
        if man_wish == index:
            happy.add(index)
            seated.add(index)
        else:
            if M[man_wish] == index:
                happy.add(index)
                happy.add(man_wish)
                seated.add(index)
                seated.add(man_wish)
    return happy
        

def celeb(G):
    n = len(G)
    for u in range(n):
        for v in range(n):
            if u==v: continue
            if G[u][v]: break
            if not G[v][u]: break
        else:
            return u
    return None






def celeb2(G):
    n = len(G)
    u, v = 0, 1
    for c in range(2, n+1):
        if G[u][v]: u=c
        else: v=c
    if u==n: c=v
    else: c=u
    for v in range(n):
        if c==v: continue
        if G[c][v]: break
        if not G[v][c]: break
    else:
        return c
    return None


def main():
#   M = [2,1,0,0,5,4,3]
    M = [2,0,0,0,5,4,3]
#   A = [0,1,2,3,4,5,6]
#   print naive_max_perm(M)
#   print my_naive_max_perm(M)
    G = [[0 for _ in range(5)] for _ in range(5)]
#    for k in range(5):
#        G[k][k] = 1
#    for _ in range(25):
#        i = random.randint(0, 4)
#        j = random.randint(0, 4)
#        G[i][j] = 1
#    for line in G:
#        print line
#    G = \
#    [[1, 1, 1, 1, 1],
#     [0, 1, 0, 0, 0],
#     [1, 1, 1, 1, 1],
#     [0, 1, 1, 1, 0],
#     [0, 1, 1, 0, 1]]
    G = \
    [[1, 1, 1, 1, 1],
     [0, 1, 1, 1, 0],
     [1, 1, 1, 1, 1],
     [0, 0, 0, 1, 0],
     [0, 1, 1, 1, 1]]
    print celeb(G)
    print celeb2(G)



if __name__ == "__main__":
    main()
