#!/usr/bin/env python
from __future__ import print_function

import gevent
from gevent import monkey; monkey.patch_all()

import socket


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8888))
    while True:
        sock.send(b'ping\n')
        data = sock.recv(1024)
        print(data)
        gevent.sleep(1)


if __name__ == '__main__':
    gevent.wait([gevent.spawn(client) for _ in range(100)])
