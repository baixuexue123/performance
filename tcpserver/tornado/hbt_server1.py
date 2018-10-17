#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import signal
import time

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.tcpserver import TCPServer


@gen.coroutine
def hbt_handler(stream, address):
    print('New connection from %s:%s' % address)
    while 1:
        try:
            data = yield stream.read_until(b"\r\n")
            msg = data.decode()
            if msg == 'ping\r\n':
                yield stream.write(b'pong\r\n')
            else:
                print('ERROR: ', address, 'Received: ', msg)
                break
        except StreamClosedError:
            print('Connection(%s:%s) lost' % address)
            break


class HbtServer(TCPServer):
    """"
    这里不用加@gen.coroutine, 加了性能反而不好了
    """
    def handle_stream(self, stream, address):
        hbt_handler(stream, address)


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
