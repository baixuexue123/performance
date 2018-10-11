#!/usr/bin/env python
# -*- coding: utf-8 -*-
import errno
import functools
import socket

from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado import gen
from tornado.iostream import IOStream


@gen.coroutine
def handle_connection(connection, address):
    stream = IOStream(connection)
    while 1:
        try:
            message = yield stream.read_until(b'\n')
            print("message from client:", message.decode().strip())
            yield stream.write(b'pong\n')
        except StreamClosedError:
            print("Lost client at host %s" % str(address))
            break
        except Exception as e:
            print(e)


def connection_ready(sock, fd, events):
    while 1:
        try:
            connection, address = sock.accept()
        except socket.error as e:
            if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                raise
            return
        connection.setblocking(0)

        handle_connection(connection, address)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    sock.bind(("", 8080))
    sock.listen(128)

    io_loop = IOLoop.current()
    callback = functools.partial(connection_ready, sock)
    io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
    io_loop.start()
