# -*- coding=utf-8 -*-





import Tkinter as tk


class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.bind("<F3>", self.toggle_catalog)

    def toggle_catalog(self, e):
        pass

    def start(self):
        self.mainloop()




        

class BaseEditor(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        self.t = tk.Text(self, wrap=tk.NONE)
        self.create_tags()

    def set_cur_status(self, status):
        self.cur_status = status

    def create_tags(self):
        self.t.tag_config("highlight",
                          background = "yellow")
        self.t.tag_config("syntax_blue",
                          background = "blue")

        self.t.tag_config("node_dir",
                          foreground = "red")
        self.t.tag_config("node_file",
                          foreground = "blue")

    def remove_highlight(self, index1, index2 = None):
        self.t.tag_remove("highlight", index1, index2)

    def add_highlight(self, index1, index2 = None):
        self.t.tag_add("highlight", index1, index2)


if __name__ == "__main__":
    w = Window()
    w.start()
        
