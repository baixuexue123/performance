#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import logging
from time import time

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.options import options, define
from tornado.tcpclient import TCPClient

define("host", default="localhost", help="TCP server host")
define("port", default=8080, help="TCP port to connect to")
define("message", default="ping", help="Message to send")

logger = logging.getLogger(__name__)


@gen.coroutine
def send_message(flag):
    stream = yield TCPClient().connect(options.host, options.port)
    while 1:
        message = options.message + ': %s : %s\n' % (time(), flag)
        try:
            yield stream.write(message.encode())
            print("Sent to server:", options.message)
            reply = yield stream.read_until(b"\n")
            print("Response from server:", reply.decode().strip())
        except StreamClosedError:
            logger.warning("Lost connection")
            break
        except Exception as e:
            print(e)

        yield gen.sleep(0.5)


if __name__ == "__main__":
    options.parse_command_line()

    io_loop = IOLoop.current()

    for i in range(100):
        # io_loop.spawn_callback(send_message, i)
        # io_loop.add_future(send_message(i), callback=lambda: None)
        send_message(i)

    io_loop.start()
