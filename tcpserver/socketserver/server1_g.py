#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
gevent.monkey.patch_all()
patches stdlib (including socket and ssl modules) to cooperate with other greenlets
"""

import gevent.monkey; gevent.monkey.patch_all()

import socket
import threading


def echo(sock):
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            sock.sendall(data)
    finally:
        sock.close()


def serve(addr):
    sock = socket.socket()
    sock.bind(addr)
    sock.listen(50)
    while True:
        conn, _ = sock.accept()
        threading.Thread(target=echo, args=(conn,)).start()


serve(('0.0.0.0', 8888))
