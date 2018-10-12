#!/usr/bin/env python
from __future__ import print_function

from gevent import socket
from gevent.server import StreamServer


# this handler will be run for each incoming connection in a dedicated greenlet
def echo(sock, address):
    print('New connection from %s:%s' % address)
    sock.sendall(b'Welcome to the echo server! Type quit to exit.\r\n')
    # using a makefile because we want to use readline()
    rfileobj = sock.makefile(mode='rb')
    while True:
        line = rfileobj.readline()
        if not line:
            print("client disconnected")
            break
        if line.strip().lower() == b'quit':
            print("client quit")
            break
        sock.sendall(line)
        print("echoed %r" % line)

    sock.shutdown(socket.SHUT_WR)
    rfileobj.close()


if __name__ == '__main__':
    # to make the server use SSL, pass certfile and keyfile arguments to the constructor
    server = StreamServer(('127.0.0.1', 8888), echo)
    # to start the server asynchronously, use its start() method;
    # we use blocking serve_forever() here because we have no other jobs
    print('Starting echo server on port 8888')
    server.serve_forever()
