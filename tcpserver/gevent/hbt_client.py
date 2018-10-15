#!/usr/bin/env python
from __future__ import print_function

import gevent
from gevent import monkey; monkey.patch_all()

import socket
import time

TOTAL = []
MAX = []
AVG = []


def client(i):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 8888))
    client_name = 'thread-%s' % i
    elapsed = []
    cnt = 10
    reader = sock.makefile('rb', newline='\r\n')
    start = time.time()
    while True:
        st = time.time()
        sock.send(b'ping\r\n')
        reply = reader.readline()
        if reply != b'pong\r\n':
            print(client_name, ' - ', time.time()-st, ' ERROR: ', reply)
            break
        elapsed.append(time.time() - st)
        cnt -= 1
        if cnt <= 0:
            break
        gevent.sleep(1)

    reader.close()
    sock.close()
    TOTAL.append(time.time()-start)
    MAX.append(max(elapsed))
    AVG.append(sum(elapsed)/len(elapsed))
    # print(client_name, ' - ',
    #       'TOTAL: %s' % (time.time()-start),
    #       'MAX: %s' % max(elapsed),
    #       'AVG: %s' % (sum(elapsed)/len(elapsed)))


if __name__ == '__main__':
    start = time.time()
    clients = 5000
    gevent.wait([gevent.spawn(client, i) for i in range(clients)])
    print('clients: ', clients)
    print('='*32, time.time()-start, '='*32)
    print('*'*24, 'TOTAL', '*'*24)
    print('MAX: %s\nAVG: %s\nMIN: %s\n' % (max(TOTAL), (sum(TOTAL)/len(TOTAL)), min(TOTAL)))
    print('*'*24, 'MAX', '*'*24)
    print('MAX: %s\nAVG: %s\nMIN: %s\n' % (max(MAX), (sum(MAX)/len(MAX)), min(MAX)))
    print('*'*24, 'AVG', '*'*24)
    print('MAX: %s\nAVG: %s\nMIN: %s\n' % (max(AVG), (sum(AVG)/len(AVG)), min(AVG)))
