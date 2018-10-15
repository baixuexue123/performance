#!/usr/bin/env python
import asyncio


class HbtProtocol(asyncio.Protocol):

    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        print('New connection from {}'.format(self.peername))
        self.transport = transport

    def data_received(self, data):
        msg = data.decode()
        if msg == 'ping\r\n':
            self.transport.write(b'pong\r\n')
        else:
            print('ERROR: ', self.peername, 'Received: ', msg)

    def connection_lost(self, exc):
        print('Lost connection of {}'.format(self.peername))
        self.transport.close()


loop = asyncio.get_event_loop()
coro = loop.create_server(HbtProtocol, '0.0.0.0', 8888)
server = loop.run_until_complete(coro)

print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
