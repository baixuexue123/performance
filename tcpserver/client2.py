#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import signal
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
def main():
    stream = yield TCPClient().connect(options.host, options.port)
    while 1:
        message = options.message + ': %s\n' % time()
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

        yield gen.sleep(1.0)


def sig_handler(sig, frame):
    logger.warning('Caught signal: %s', sig)
    IOLoop.current().add_callback_from_signal(IOLoop.current().stop)


if __name__ == "__main__":
    options.parse_command_line()
    io_loop = IOLoop.current()

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    IOLoop.current().run_sync(main)
