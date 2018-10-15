#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey; monkey.patch_all()

import socketserver


class HbtHandler(socketserver.StreamRequestHandler):

    def setup(self):
        super(HbtHandler, self).setup()
        print('New connection from %s:%s' % self.client_address)

    def handle(self):
        for line in self.rfile:
            if line == b'ping\r\n':
                self.wfile.write(b'pong\r\n')
            else:
                print('ERROR: ', self.client_address, 'Received: ', line)

    def finish(self):
        super(HbtHandler, self).finish()
        print('Connection(%s:%s) lost' % self.client_address)


class HbtServer(socketserver.ThreadingTCPServer):
    request_queue_size = 20000


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "127.0.0.1", 8888

    with HbtServer((HOST, PORT), HbtHandler) as server:
        server.serve_forever()


# clients:  1000
# ================================ 10.875595808029175 ================================
# ************************ TOTAL ************************
# MAX: 9.619552612304688
# AVG: 9.251795869350433
# MIN: 9.042979955673218
#
# ************************ MAX ************************
# MAX: 0.5692858695983887
# AVG: 0.18562082505226135
# MIN: 0.007962226867675781
#
# ************************ AVG ************************
# MAX: 0.058420205116271974
# AVG: 0.021565202331542972
# MIN: 0.0015587329864501954


# clients:  5000
# ================================ 15.086085557937622 ================================
# ************************ TOTAL ************************
# MAX: 12.136761665344238
# AVG: 9.4151985809803
# MIN: 9.081790685653687
#
# ************************ MAX ************************
# MAX: 3.042595863342285
# AVG: 0.23480255093574523
# MIN: 0.010228633880615234
#
# ************************ AVG ************************
# MAX: 0.3092873334884644
# AVG: 0.03424973369121559
# MIN: 0.0029220104217529295


# clients 10000  BAD
