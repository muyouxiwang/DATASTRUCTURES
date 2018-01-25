# -*- coding=utf-8 -*-

import os

import re




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
            catalog_info += catalog_1(p, depth)
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


class Content(object):
    def __init__(self, path):
        self.path = path

        with open(self.path, "r") as rf:
            self.content = rf.read()
        self.content_lines = self.content.split("\n")

    def get_content(self):
        return self.content

    def search_all(self, s, p):
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

    def search(self, s):
        searched = set()
        if s:
            for i, line in enumerate(self.content_lines):
                for j in self.search_all(line, s):
                    searched.add((i, j))
        return searched


    def get_next_word(self, x, y):
        line = self.content_lines[x][y:]
        p = re.compile("[a-zA-Z_]+")
        d = p.search(line)
        if d:
            return (x, d.span()[1] + y)
        else:
            return (x + 1, 0)


    def get_word_end(self, x, y):
        line = self.content_lines[x][y:]
        p = re.compile("[a-zA-Z_]+")
        if line:
            start = False
            for i, c in enumerate(line):
                if p.search(c) is None:
                    if start:
                        return (x, y + i)
                    else:
                        continue
                else:
                    start = True
            return (x + 1, 0)
        else:
            return (x + 1, 0)


    def get_close_char(self, x, y, start_c, end_c):
        x1, y1, x2, y2 = -1, -1, -1, -1
        for i in range(x):
            t_x = x - i
            line = self.content_lines[t_x]
            if t_x == x:
                line = line[:y+1]
            index = line.rfind(start_c)
            if index != -1:
                x1 = t_x
                y1 = index
                break
        
        for i in range(len(self.content_lines) - x):
            t_x = x + i
            line = self.content_lines[t_x]
            if t_x == x:
                line = line[y:]
            index = line.find(end_c)
            if index != -1:
                x2 = t_x
                if t_x == x:
                    y2 = index + y
                else:
                    y2 = index
                break
        return x1, y1, x2, y2


        



#def get_content():
    #content = []
    #count = 1
    #with open("./code_demo.py", "r") as r:
        #for line in r:
            #line = "%d: %s" % (count, line)
            #content.append(line)
            #count += 1
    #return "".join(content)

