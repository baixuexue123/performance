#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent.server import StreamServer
from gevent.pool import Pool


def echo_handler(sock, address):
    print('New connection from %s:%s' % address)
    for l in sock.makefile('r'):
        print(address, " : ", l)
        sock.sendall(l.encode())


if __name__ == '__main__':
    pool = Pool(10000)  # do not accept more than 10000 connections
    server = StreamServer(('0.0.0.0', 8888), echo_handler, spawn=pool)
    server.serve_forever()
