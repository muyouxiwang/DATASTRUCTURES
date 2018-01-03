# -*- coding=utf-8 -*-








class Union(object):
    def __init__(self, n):
        self.ends = {}
        for i in range(1, n + 1):
            self.ends[i] = i
    
    def find(self, p):
        return self.ends[p]

    def union(self, p, q):
        pid = self.find(p)
        qid = self.find(q)
        if pid == qid:
            return
        for k, v in self.ends.iteritems():
            if v == pid:
                self.ends[k] = qid

    def connected(self, p, q):
        return self.find(p) == self.find(q)





class QuickUnion(object):
    def __init__(self):
        self.ends = {}
        for i in range(1, n + 1):
            self.ends[i] = i

    def find(self, p):
        while p != self.ends[p]:
            p = self.ends[p]
        return p
    
    def union(self, p, q):
        pid = self.quick_find(p)
        qid = self.quick_find(q)
        if pid != qid:
            self.ens[p] = q

    def connected(self, p, q):
        return self.quick_find(p) == self.quick_find(q)




def main():
    u = Union(500)
    u.union(5, 8)
    u.union(9, 8)
    u.union(7, 8)
    u.union(1, 300)
    u.union(4, 154)
    u.union(152, 4)
    u.union(99, 200)
    return u
    





if __name__ == "__main__":
    main()
