# -*- coding=utf-8 -*-

import make_graphic

def _visit(node):
    print node

class Node(object):
    def __init__(self, k, v):
        self.k = k
        self.left = None
        self.right = None
        self.v = v
    
    def __str__(self):
        return str(self.k)

    def get_ages(self):
        ages = []
        if self.left:
            ages.append((self, self.left))
        if self.right:
            ages.append((self, self.right))
        return ages

    __repr__ = __str__


class HashTable(object):
    def __init__(self):
        self.root = None

    def get(self, k):
        return self._get(self.root, k)

    def _get(self, node, k):
        if node is None:
            return None
        elif k == node.k:
            return node.v
        elif k > node.k:
            return self._get(node.right, k)
        elif k < node.k:
            return self._get(node.left, k)

    def put(self, k, v):
        self.root = self._put(self.root, k, v)
 
    def _put(self, node, k, v):
        if node is None:
            node = Node(k, v)
        elif k == node.k:
            node.v = v
        elif k > node.k:
            node.right = self._put(node.right, k, v)
        elif k < node.k:
            node.left = self._put(node.left, k, v)
        node.N = 1 + self._leth(node.left) + self._leth(node.right)
        return node

    def leth(self):
        return self._leth(self.root)

    def _leth(self, node):
        if node is None:
            return 0
        return node.N

    def pre_trav(self):
        self._pre_trav(self.root)

    def _pre_trav(self, node, visit = _visit):
        if node is None:
            return
        visit(node)
        self._pre_trav(node.left, visit)
        self._pre_trav(node.right, visit)
    
    def mid_trav(self):
        self._mid_trav(self.root)

    def _mid_trav(self, node, visit = _visit):
        if node is None:
            return
        self._mid_trav(node.left, visit)
        visit(node) 
        self._mid_trav(node.right, visit)
 
    def pos_trav(self):
        self._pos_trav(self.root)

    def _pos_trav(self, node, visit = _visit):
        if node is None:
            return
        self._pos_trav(node.left, visit)
        self._pos_trav(node.right, visit)
        visit(node)

    def show(self):
        nodes = []
        ages = set()
        def _visit(node):
            nodes.append(node)
            ages.update(node.get_ages())
        self._pre_trav(self.root, _visit)
        make_graphic.see_pic(make_graphic.make_tree_content(nodes, ages))

    

def test():
    d = HashTable()
    d.put(3, 4)
    d.put(5, 6)
    d.put(2, 8)
    d.put(1, 7)
    d.put(8, 9)
    assert(d.leth() == 5)
    d.put(4, 10)
    assert(d.leth() == 6)
    d.put(9, 10)
    d.put(7, 15)
    d.put(9, 14)
    assert(d.leth() == 8)

    assert(d.get(3) == 4)
    assert(d.get(5) == 6)
    assert(d.get(1) == 7)
    assert(d.get(2) == 8)
    
    #d.show()


if __name__ == "__main__":
    test()








