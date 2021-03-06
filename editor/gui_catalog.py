# -*- coding=utf-8 -*-

import Tkinter as tk
import edit

import gui
import editor_status



class GuiCatalog(gui.BaseEditor):
    def __init__(self, root):
        gui.BaseEditor.__init__(self, root)

        self.t.pack()

        self.pack()

        self.t.bind("<o>", self.toggle_node)
        self.t.bind("<x>", self.close_parent_node)

        self.t.config(cursor = "arrow",
                #insertwidth = 10,
                insertbackground = "brown")


        self.tags = set()


    def set_cur_status(self, status):
        self.cur_status = status

    def create_catalog(self, root_path):
        self.catalog = edit.Catalog(root_path)




    def toggle_node(self, e):
        print "toggle_nod  ..."
        return "break"

    def close_parent_node(self, e):
        print "close parent ..."
        return "break"
            

    # def show(self):
    #     self.t.delete("1.0", tk.END)
    #     i = 1
    #     for n, p in self.catalog.get_whole_content():
    #         self.t.insert("%d.0" % i, n)
    #         self.t.tag_add(p, "%d.0" % i, "%d.%d" % (i, len(n)))
    #         i += 1

    #         self.t.tag_bind(p, '<Button-1>', self.get_refresh(p))

    #         if n.strip().startswith("+"):
    #             self.t.tag_config(p, foreground = "red")
    #         if n.strip().startswith("*"):
    #             self.t.tag_config(p, foreground = "blue")


    def add_tag(self, name, index1, index2):
        self.tags.add()

    def get_refresh(self, i, node):
        def _(e):
            node.toggle()
            self.show(i, node)
        return _

    def show_catalog(self):
        self.show(1, self.catalog.root)
        

    def show(self, i, pnode):
        self.clear_syntax(i)

        self.t.delete("%d.0" % i, "end")
        self.t.insert("end", "\n")
        for node in self.catalog.get_content(pnode):
            start_index = "%d.0" % i
            self.t.insert(start_index, node.name)
            self.t.tag_add(node.abspath, start_index, "%d.%d" % (i, len(node.name)))
            self.t.tag_bind(node.abspath, '<Button-1>', self.get_refresh(i, node))

            self.syntax_node(node.ntype,
                    start_index, start_index + " lineend")
            i += 1


    def syntax_node(self, ntype, index1, index2):
        self.tags.add((ntype, index1, index2))
        self.t.tag_add(ntype, index1, index2)


    def clear_syntax(self, cur_line):
        for ntype, index1, index2 in self.tags:
            line = int(float(index1))
            if line >= cur_line:
                self.t.tag_remove(ntype, index1, index2)
                
            

if __name__ == "__main__":
    dir_path = "E:/svn_hs2_gm"


    root = tk.Tk()
    gui = GuiCatalog(root)
    gui.create_catalog(dir_path)
    gui.show_catalog()
    # catalog.set_cur_status(editor_status.NormalStatus(
                            # catalog, catalog.t))
    root.mainloop()

