#!/usr/bin/env python
import asyncio
import time

TOTAL = []
MAX = []
AVG = []


async def tcp_echo_client(n, loop):
    client_name = 'thread-%s' % n
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888, loop=loop)

    elapsed = []
    start = time.time()
    for _ in range(10):
        st = time.time()
        writer.write(b'ping\r\n')
        reply = await reader.readuntil(b'\r\n')
        if reply != b'pong\r\n':
            print(client_name, ' - ', time.time()-st, ' ERROR: ', reply)
            break
        elapsed.append(time.time() - st)
        await asyncio.sleep(1, loop=loop)

    writer.close()
    TOTAL.append(time.time()-start)
    MAX.append(max(elapsed))
    AVG.append(sum(elapsed)/len(elapsed))


clients = 5000
start = time.time()
loop = asyncio.get_event_loop()
tasks = [tcp_echo_client(i, loop) for i in range(clients)]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

print('clients: ', clients)
print('='*32, '%.4f' % (time.time()-start), '='*32)
print('*'*24, 'TOTAL', '*'*24)
print('MAX: %.4f\nAVG: %.4f\nMIN: %.4f\n' % (max(TOTAL), (sum(TOTAL)/len(TOTAL)), min(TOTAL)))
print('*'*24, 'MAX', '*'*24)
print('MAX: %.4f\nAVG: %.4f\nMIN: %.4f\n' % (max(MAX), (sum(MAX) / len(MAX)), min(MAX)))
print('*'*24, 'AVG', '*'*24)
print('MAX: %.4f\nAVG: %.4f\nMIN: %.4f\n' % (max(AVG), (sum(AVG) / len(AVG)), min(AVG)))
