#!/usr/bin/env python
from __future__ import print_function

import gevent
from gevent import monkey; monkey.patch_all()

import socket
import time


def client(i):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 8888))
    client_name = 'thread-%s' % i
    while True:
        st = time.time()
        sock.send(b'ping\r\n')
        reply = sock.recv(1024)
        elapsed = time.time()-st
        print(client_name, ' - ', elapsed, ' REPLY: ', reply)
        gevent.sleep(1)


if __name__ == '__main__':
    gevent.wait([gevent.spawn(client, i) for i in range(1000)])
