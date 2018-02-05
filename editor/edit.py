# -*- coding=utf-8 -*-

import os

import re


class Tree(object):
    def __init__(self, name, abspath, ntype = "dir", depth = 0, toggle = False):
        self.name = "+%s" % name if ntype == "dir" else "*%s" % name
        self._toggle = toggle
        self.children = []
        self.ntype = ntype
        self.depth = depth

        self.name = self.depth * "    " + self.name + "\n"
        self.abspath = abspath

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
            


            
class Catalog(object):
    def __init__(self, root_path):
        self.the_catalog = {}
        self.root_path = os.path.abspath(root_path)
        root = Tree(os.path.basename(self.root_path),
                    self.root_path,
                    toggle=True)
        self.the_catalog[root.abspath] = root
        self.create_catalog(self.root_path, root)

        self.root = root

    def get_content(self, ap):
        return self.the_catalog[ap].get_series()
        # return self.root.get_series()

    def get_whole_content(self):
        return self.get_content(self.root_path)


    def toggle_node(self, node_path):
        self.the_catalog[node_path].toggle()


    def create_catalog(self, d, node, depth = 0):
        depth += 1
        for n in os.listdir(d):
            if n.startswith("."):
                continue
            p = os.path.join(d, n)
            if os.path.isdir(p):
                c = Tree(n, p, "dir", depth)
                self.the_catalog[c.abspath] = c
                node.add_child(c)
                self.create_catalog(p, c, depth)
            else:
                t = Tree(n, p, "file", depth)
                self.the_catalog[t.abspath] = t
                node.add_child(t)
        return node



class Content(object):
    def __init__(self, path):
        self.path = path

        self.saved = True
        self.content_lines = []
        self.content = ""

        with open(self.path, "r") as rf:
            for line in rf:
                self.content_lines.append(line)
                self.content += line

    def get_content(self):
        return self.content

    def _search_all(self, s, p):
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
                for j in self._search_all(line, s):
                    searched.add((i, j))
        return searched


    def get_next_word(self, x, y):
        line = self.content_lines[x][y+1:]
        p = re.compile("[a-zA-Z_]+")
        d = p.search(line)
        if d:
            return (x, d.span()[0] + y + 1)
        else:
            return (x + 1, 0)

    def index_to_pos(self, index):
        if index < 0 or index > len(self.content):
            return (-1, -1)
        for i, line in enumerate(self.content_lines):
            if index <= len(line):
                return (i, index)
            index -= len(line)

    def pos_to_index(self, x, y):
        if x > len(self.content_lines):
            return -1
        if len(self.content_lines[x]) < y:
            return -1
        index = 0
        for i in range(x):
            index += len(self.content_lines[i])
        return index + y 
        


    def get_word_end(self, x, y):
        index = self.pos_to_index(x, y)
        if index == -1:
            print "nothing"
            return
        
        p = re.compile("[ \t\n\r]+")

        inword = True if p.search(self.content[index]) is None else False


        
        if inword:
            d = p.search(self.content[index+1:])
            dis = d.span()[0]
            if dis == 1:
                return self.get_word_end(x, y + 1)
            index += d.span()[0]
            return self.index_to_pos(index)
        else:
            i = index + 1
            while p.search(self.content[i]) is not None:
                i += 1

            x1, y1 = self.index_to_pos(i)
            return self.get_word_end(x1, y1)
            
        
        # if line:
        #     start = False
        #     for i, c in enumerate(line):
        #         if p.search(c) is None:
        #             if start:
        #                 return (x, y + i)
        #             else:
        #                 continue
        #         else:
        #             start = True
        #     return (x + 1, 0)
        # else:
        #     return (x + 1, 0)


    def get_word_start(self, x, y):
        line = self.content_lines[x][:y]
        p = re.compile("[a-zA-Z_]+")
        max = 0
        if line:
            for i, c in enumerate(line):
                if p.search(c) is None:
                    if i > max:
                        max = i
            return (x, max)
        else:
            return (x, 0)


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


# def catalog_1(d, depth = 0):
#     depth += 1
#     catalog_info = "+%s\n" % os.path.basename(d)
#     ns = os.listdir(d)
#     for n in ns:
#         if n.startswith("."):
#             continue
#         p = os.path.join(d, n)
#         if os.path.isdir(p):
#             catalog_info += catalog_1(p, depth)
#         else:
#             catalog_info += "%s-%s\n" % (depth * " ", n) 
#     return catalog_info

