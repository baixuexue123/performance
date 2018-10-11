#!/usr/bin/env python
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado import gen
from tornado.options import define, options, parse_command_line


class IndexHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        yield gen.sleep(0.1)
        self.set_status(200)
        self.set_header("Content-Type", "text/html")
        self.write("<p>Hello World</p>")


def make_app():
    return tornado.web.Application(
        [(r"/", IndexHandler)],
        debug=False
    )


def main():
    define("port", default=8000, help="run on the given port", type=int)
    parse_command_line()

    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port, address="127.0.0.1")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
