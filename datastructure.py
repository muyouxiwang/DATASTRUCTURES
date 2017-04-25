# -*- coding=utf-8 -*-

import make_graphic

def _visit(node):
    print node,

class Node(object):
    def __init__(self, k, v):
        self.k = k
        self.left = None
        self.right = None
        self.v = v
        self.parent = None
    
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
            new_node = self._put(node.right, k, v)
            node.right = new_node
            new_node.parent = node
        elif k < node.k:
            new_node = self._put(node.left, k, v)
            node.left = new_node
            new_node.parent = node
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
        print

    def _pre_trav(self, node, visit = _visit):
        if node is None:
            return
        visit(node)
        self._pre_trav(node.left, visit)
        self._pre_trav(node.right, visit)
    
    def mid_trav(self):
        self._mid_trav(self.root)
        print

    def _mid_trav(self, node, visit = _visit):
        if node is None:
            return
        self._mid_trav(node.left, visit)
        visit(node) 
        self._mid_trav(node.right, visit)
 
    def pos_trav(self):
        self._pos_trav(self.root)
        print

    def _pos_trav(self, node, visit = _visit):
        if node is None:
            return
        self._pos_trav(node.left, visit)
        self._pos_trav(node.right, visit)
        visit(node)

    def min(self):
        if self.root is None:
            return None
        return self._min(self.root).k

    def _min(self, node):
        if node.left is None:
            return node
        return self._min(node.left)

    def max(self):
        if self.root is None:
            return None
        return self._max(self.root).k

    def _max(self, node):
        if node.right is None:
            return node
        return self._max(node.right)

    def rank(self, k):
        return self._rank(self.root, k)

    def _rank(self, node, k):
        if k == node.k:
            return self._leth(node.left) + 1
        elif k < node.k:
            return self._rank(node.left, k)
        else:
            return self._leth(node.left) + 1 + self._rank(node.right, k)

    def select(self, ranknum):
        return self._select(self.root, ranknum)

    def _select(self, node, ranknum):
        if node is None:
            return None
        num = self.rank(node.k)
        if num == ranknum:
            return node.k
        elif num < ranknum:
            return self._select(node.right, ranknum)
        else:
            return self._select(node.left, ranknum)

    def delete_min(self):
        self._delete_min(self.root)

    def _delete_min(self, node):
        if node is None:
            return
        next = node.left
        if next:
            self._delete_min(next)
        else:
            if node.right:
                node.parent.left = node.right
                #node = node.right
            else:
                #node = None
                node.parent.left = None
 
    def delete_max(self):
        self._delete_max(self.root)

    def _delete_max(self, node):
        if node is None:
            return
        next = node.right
        if next:
            self._delete_max(next)
        else:
            if node.left:
                #node = node.left
                node.parent.right = node.left
            else:
                #node = None
                node.parent.right = None
        

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

    assert(d.min() == 1)
    assert(d.max() == 9)
    
    #d.show()
    d.mid_trav()

    d.delete_min()
    #d.show()
    d.mid_trav()

    d.delete_max()
    #d.show()
    d.mid_trav()

    d.delete_max()
    d.mid_trav()

    d.delete_min()
    d.mid_trav()

    # print d.rank(9)
    # print d.rank(8)
    # print d.rank(5)
    # print d.rank(7)

    # print d.select(6)
    # print d.select(7)
    # print d.select(8)
    # print d.select(10)





if __name__ == "__main__":
    test()








