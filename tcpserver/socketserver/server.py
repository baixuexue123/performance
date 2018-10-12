#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
blocking (no IO multiplexing)
"""

import socket


def echo(sock):
    try:
        while True:
            data = sock.recv(1024)  # blocks until recieve data.
            if not data:
                break
            sock.sendall(data)  # block until send buffer is not full.
    finally:
        sock.close()


def serve(addr):
    sock = socket.socket()
    sock.bind(addr)
    sock.listen(50)
    while True:
        conn, _ = sock.accept()  # block until client comes.
        echo(conn)  # doesn't return until client disconnect.


serve(('0.0.0.0', 8888))
