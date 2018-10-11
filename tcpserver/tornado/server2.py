#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import signal
import time

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer
from tornado.log import gen_log
from tornado.options import parse_command_line


class Handler(object):
    clients = set()

    def __init__(self, stream, address):
        Handler.clients.add(self)
        self._stream = stream
        self._address = address
        self._stream.set_close_callback(self.on_close)
        gen_log.info("A new user has entered the chat room.")

    @gen.coroutine
    def read_message(self):
        message = yield self._stream.read_until(b'\n')
        gen_log.info("User%s said -- %s" % (self._address, message))
        return message

    @gen.coroutine
    def broadcast_messages(self, data):
        for c in Handler.clients:
            yield c.send_message(data)

    @gen.coroutine
    def send_message(self, data):
        return self._stream.write(data)

    def on_close(self):
        gen_log.info("A user has left the chat room. %s" % str(self._address))
        Handler.clients.remove(self)

    @gen.coroutine
    def serve(self):
        while 1:
            try:
                message = yield self.read_message()
                self.broadcast_messages(message)
            except StreamClosedError:
                print("Lost client at host %s" % str(self._address))
                break
            except Exception as e:
                print(e)


class ChatServer(TCPServer):
    @gen.coroutine
    def handle_stream(self, stream, address):
        gen_log.info("New connection : %s %s" % (address, stream))
        gen_log.info("clients num is: %s" % len(Handler.clients))
        h = Handler(stream, address)
        h.serve()


def sig_handler(sig, frame):
    """ Catch signal and init callback. """
    gen_log.warning('Caught signal: %s' % sig)
    IOLoop.current().add_callback(shutdown)


def shutdown():
    """Stop server and add callback to stop i/o loop"""
    io_loop = IOLoop.current()
    gen_log.info('Will shutdown in 1 seconds ...')
    io_loop.add_timeout(time.time() + 1, io_loop.stop)


if __name__ == '__main__':
    parse_command_line()
    gen_log.info("Server start ......")
    io_loop = IOLoop.current()

    server = ChatServer()
    server.listen(8080)

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    io_loop.start()
