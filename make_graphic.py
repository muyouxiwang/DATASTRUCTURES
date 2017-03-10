# -*- coding=utf-8 -*-

import os




def make_tree_content(nodes, ages):
    def _make_node(node):
        return "node%s[label=\"{%s|%s}\"]" % (node.k, node.k, node.v)
    def _make_age(nodea, nodeb):
        return "node%s->node%s" % (nodea.k, nodeb.k)

    graphic_temp = """
    digraph G{
    node[shape=record]
    %s
    }
    """

    content = "\n".join([_make_node(node) for node in nodes])
    content += "\n"
    content += "\n".join([_make_age(*age) for age in ages])
    content = graphic_temp % content
    return content

def see_pic(content, filename = "tmp"):
    with open("%s.gv" % filename, "w") as wf:
        wf.write(content)
    os.system("dot %s.gv -Tpng -o %s.png" % (filename, filename))
    os.startfile("%s.png" % filename)
 
 

if __name__ == "__main__":
    import datastructure
    nodea = datastructure.Node(3, 8)
    nodeb = datastructure.Node(5, 9)


    see_pic(make_tree_content([nodea, nodeb], [(nodea, nodeb), ]))






