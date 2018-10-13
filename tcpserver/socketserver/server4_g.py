#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()

import threading
import socketserver


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            data = self.request.recv(1024)
            if not data:
                break
            cur_thread = threading.current_thread()
            response = "{}: {}\r\n".format(cur_thread.name, data)
            self.request.sendall(response.encode())


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 8888

    with ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler) as server:
        ip, port = server.server_address
        print("Server loop running in thread:", threading.current_thread().name)
        server.serve_forever()
