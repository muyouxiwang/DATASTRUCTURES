# -*- coding=utf-8 -*-

import os




the_catalog = {}

root_dir = "E:/svn_hs2_gm"


class Tree(object):
    def __init__(self, name, abspath, ntype = "dir", depth = 0, toggle = False):
        self.name = "+%s" % name if ntype == "dir" else "*%s" % name
        self._toggle = toggle
        self.children = []
        self.ntype = ntype
        self.depth = depth

        self.name = self.depth * "    " + self.name + "\n"
        self.abspath = abspath

        the_catalog[self.abspath] = self

    def toggle(self):
        self._toggle = not self._toggle
        

    def add_child(self, c):
        self.children.append(c)

    def __str__(self):
        if self._toggle and self.ntype == 'dir':
            print self.name + "".join([str(c) for c in self.children])
            return self.name + "".join([str(c) for c in self.children])
        return self.name

    __repr__ = __str__

    def get_series(self):
        t = [(self.name, self.abspath),]
        if self._toggle and self.ntype == 'dir':
            for n in [c.get_series() for c in self.children]:
                t.extend(n)
        return t
            


def catalog_1(d, depth = 0):
    depth += 1
    catalog_info = "+%s\n" % os.path.basename(d)
    ns = os.listdir(d)
    for n in ns:
        if n.startswith("."):
            continue
        p = os.path.join(d, n)
        if os.path.isdir(p):
            catalog_info += catalog(p, depth)
        else:
            catalog_info += "%s-%s\n" % (depth * " ", n) 
    return catalog_info

def catalog(d, node, depth = 0):
    depth += 1
    for n in os.listdir(d):
        if n.startswith("."):
            continue
        p = os.path.join(d, n)
        if os.path.isdir(p):
            c = Tree(n, p, "dir", depth)
            node.add_child(c)
            catalog(p, c, depth)
        else:
            node.add_child(Tree(n, p, "file", depth))
    return node
            

def create_catalog():
    global root
    root = Tree(os.path.basename(root_dir), os.path.abspath(root_dir), toggle=True)
    catalog(root_dir, root)



def get_content():
    with open("./code_demo.py", "r") as r:
        content = r.read()
    return content

def search_all(s, p):
    result = []
    cur = 0
    while s:
        index = s.find(p)
        if index == -1:
            break
        result.append(index + cur)
        cur += index + len(p)
        s = s[index + len(p): ]
    return result

def search(s):
    content = get_content().split("\n")
    searched = set()
    if s:
        for i, line in enumerate(content):
            for j in search_all(line, s):
                searched.add((i, j))
    return searched





