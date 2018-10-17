#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import signal
import time

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer


class Handler(object):

    def __init__(self, stream, address):
        self._stream = stream
        self._address = address
        print('New connection from %s:%s' % address)

    @gen.coroutine
    def read_message(self):
        message = yield self._stream.read_until(b'\r\n')
        return message.decode()

    @gen.coroutine
    def send_message(self, data):
        return self._stream.write(data.encode())

    @gen.coroutine
    def serve(self):
        while 1:
            try:
                msg = yield self.read_message()
                if msg == 'ping\r\n':
                    yield self.send_message('pong\r\n')
                else:
                    print('ERROR: ', self._address, 'Received: ', msg)
                    break
            except StreamClosedError:
                print('Connection(%s:%s) lost' % self._address)
                break


class HbtServer(TCPServer):
    def handle_stream(self, stream, address):
        Handler(stream, address).serve()


def sig_handler(sig, frame):
    """Catch signal and init callback. """
    IOLoop.current().add_callback(shutdown)


def shutdown():
    """Stop server and add callback to stop i/o loop"""
    io_loop = IOLoop.current()
    io_loop.add_timeout(time.time() + 1, io_loop.stop)


if __name__ == '__main__':
    server = HbtServer()
    server.listen(8888, address='127.0.0.1')
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    IOLoop.current().start()
