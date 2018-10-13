#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
blocking (no IO multiplexing)
"""
from __future__ import print_function

import time
import socket


def echo(sock, addr):
    print('New connection from %s:%s' % addr)
    try:
        while True:
            data = sock.recv(1024)  # blocks until receive data.
            print(time.time(), "Received: ", len(data), ' - ', data, '\n')
            if not data:
                # 如果连接断开, recv会返回一个空数据
                break
            sock.sendall(b"pong\r\n")  # block until send buffer is not full.
    finally:
        sock.close()


def echo2(sock, addr):
    print('New connection from %s:%s' % addr)
    cnt = 1
    # 如过对端接收完所有数据后, 关闭连接, 那么sock.makefile将安全结束迭代
    # 否则, 将抛出异常ConnectionResetError: [Errno 104] Connection reset by peer
    for line in sock.makefile('r', newline='\r\n'):
        print(time.time(), "Received: ", len(line.encode()), ' - ', line)
        sock.send(("pong%s\r\n" % cnt).encode())
        cnt += 1
    else:
        print('disconnected')
        sock.close()


def serve(addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(addr)
    sock.listen(50)
    try:
        while True:
            conn, addr = sock.accept()  # block until client comes.
            echo2(conn, addr)  # doesn't return until client disconnect.
    finally:
        sock.close()


serve(('127.0.0.1', 8888))
