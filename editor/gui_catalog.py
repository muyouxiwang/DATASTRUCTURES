# -*- coding=utf-8 -*-

import Tkinter as tk
import edit



edit.create_catalog()


class GuiCatalog(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        f = tk.Frame(self)
        f.pack()

        self.t = tk.Text(f)
        self.t.pack()



    def get_refresh(self, p):
        def _(e):
            if p in edit.the_catalog:
                edit.the_catalog[p].toggle()
                print "shit"
                self.show()
        return _
            

    def show(self):
        self.t.config(cursor = "arrow",
                #insertwidth = 10,
                insertbackground = "brown")
        self.t.delete("1.0", tk.END)
        i = 1
        for n, p in edit.root.get_series():
            self.t.insert("%d.0" % i, n)
            self.t.tag_add(p, "%d.0" % i, "%d.%d" % (i, len(n)))
            i += 1

            self.t.tag_bind(p, '<Button-1>', self.get_refresh(p))

            if n.strip().startswith("+"):
                self.t.tag_config(p, foreground = "red")
            if n.strip().startswith("*"):
                self.t.tag_config(p, foreground = "blue")

    def start(self):

        self.show()
        self.mainloop()


GuiCatalog().start()

