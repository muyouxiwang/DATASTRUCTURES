# -*- coding=utf-8 -*-


import tornado.web


class Game(tornado.web.RequestHandler):

    def get(self):
        pin = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1"
        self.render("gui.html", **{"pin": pin})

    def post(self):
        self.get()
