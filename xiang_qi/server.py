# -*- coding=utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.httpserver
import game


def make_app():
    settings = {"static_path" : "./static",
                }

    return tornado.web.Application([
            (r"/", game.Game),
            ], **settings)

if __name__ == "__main__":
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()













