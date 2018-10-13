#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import socket
import threading


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 8888))


def reader(fd):
    for line in fd:
        print("Received: ", line)
    fd.close()


# 单独开一个reader线程
t = threading.Thread(target=reader, args=(sock.makefile(newline='\r\n'),))
t.daemon = True  # Exit the server thread when the main thread terminates
t.start()


try:
    while True:
        msg = input("Please input msg: ")
        sock.send(b'aaa\r\nbbb\r\nccc\r\nddd\r\n')
        # reply = sock.recv(1024)  # recv有可能一次接收不全
        # print("Received: ", reply)
finally:
    sock.close()
