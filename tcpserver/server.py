#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import logging
import signal

from tornado import gen
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado.options import define, options, parse_command_line

define("port", default=9888, help="TCP port to listen on")

logger = logging.getLogger(__name__)


class EchoServer(TCPServer):
    @gen.coroutine
    def handle_stream(self, stream, address):
        while 1:
            try:
                data = yield stream.read_until(b"\n")
                logger.info("Received bytes: %s", data)
                if not data.endswith(b"\n"):
                    data = data + b"\n"
                yield stream.write(data)
            except StreamClosedError:
                logger.warning("Lost client at host %s", address[0])
                break
            except Exception as e:
                print(e)


def handle_sigchld(sig, frame):
    IOLoop.current().add_callback_from_signal(IOLoop.current().stop)


def main():
    parse_command_line()

    server = EchoServer()
    server.listen(options.port)
    logger.info("Listening on TCP port %d", options.port)
    io_loop = IOLoop.current()

    signal.signal(signal.SIGCHLD, handle_sigchld)

    def callback():
        print('---------------------')
        print(len(io_loop.handlers))

    period = PeriodicCallback(callback=callback, callback_time=500)
    period.start()

    io_loop.start()


if __name__ == "__main__":
    main()
