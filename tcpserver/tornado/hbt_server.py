#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import signal

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError


class HbtServer(TCPServer):
    @gen.coroutine
    def handle_stream(self, stream, addr):
        print('New connection from %s:%s' % addr)
        while 1:
            try:
                data = yield stream.read_until(b"\r\n")
                msg = data.decode()
                if msg == 'ping\r\n':
                    yield stream.write(b'pong\r\n')
                else:
                    print('ERROR: ', addr, 'Received: ', msg)
                    break
            except StreamClosedError:
                print('Connection(%s:%s) lost' % addr)
                break


def handle_sigchld(sig, frame):
    IOLoop.current().add_callback_from_signal(IOLoop.current().stop)


def main():
    server = HbtServer()
    server.listen(8888, address='127.0.0.1')
    print("Listening on TCP port:", 8888)
    signal.signal(signal.SIGTERM, handle_sigchld)
    signal.signal(signal.SIGINT, handle_sigchld)
    IOLoop.current().start()


if __name__ == "__main__":
    main()


# clients:  1000
# ================================ 10.90987753868103 ================================
# ************************ TOTAL ************************
# MAX: 9.40190052986145
# AVG: 9.27769600701332
# MIN: 9.205358982086182
#
# ************************ MAX ************************
# MAX: 0.16410112380981445
# AVG: 0.06533392286300659
# MIN: 0.033332109451293945
#
# ************************ AVG ************************
# MAX: 0.03371386528015137
# AVG: 0.01941330740451814
# MIN: 0.010096859931945801


# clients:  5000
# ================================ 13.934086561203003 ================================
# ************************ TOTAL ************************
# MAX: 11.224942207336426
# AVG: 9.696605278253555
# MIN: 9.232633829116821
#
# ************************ MAX ************************
# MAX: 2.006328582763672
# AVG: 0.33319732756614684
# MIN: 0.10964250564575195
#
# ************************ AVG ************************
# MAX: 0.22096095085144044
# AVG: 0.06707409784317044
# MIN: 0.022104358673095702


# clients:  10000
# ================================ 38.15929293632507 ================================
# ************************ TOTAL ************************
# MAX: 35.95339107513428
# AVG: 13.804579599571229
# MIN: 9.146072626113892
#
# ************************ MAX ************************
# MAX: 26.886558294296265
# AVG: 1.4351654207468032
# MIN: 0.05346035957336426
#
# ************************ AVG ************************
# MAX: 2.693648648262024
# AVG: 0.4675381349039068
# MIN: 0.011656618118286133
