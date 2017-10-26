#!/usr/bin/env python3
import asyncio
import uvloop
from aiohttp import web


async def handle(request):
    resp = web.Response(
        text="<p>Hello World</p>",
        content_type="text/html",
        charset="utf-8"
    )
    await asyncio.sleep(0.1)
    return resp


app = web.Application()
app.router.add_get('/', handle)
loop = uvloop.new_event_loop()
web.run_app(app, host='127.0.0.1', port=8000, loop=loop)


# ab -n 10000 -c 1000 http://127.0.0.1:8000/

# ******************** asyncio ******************
# Concurrency Level:      1000
# Time taken for tests:   3.745 seconds
# Complete requests:      10000
# Failed requests:        0
# Total transferred:      1680000 bytes
# HTML transferred:       180000 bytes
# Requests per second:    2669.98 [#/sec] (mean)
# Time per request:       374.534 [ms] (mean)
# Time per request:       0.375 [ms] (mean, across all concurrent requests)
# Transfer rate:          438.04 [Kbytes/sec] received

# ******************** uvloop *******************
# Concurrency Level:      1000
# Time taken for tests:   2.687 seconds
# Complete requests:      10000
# Failed requests:        0
# Total transferred:      1680000 bytes
# HTML transferred:       180000 bytes
# Requests per second:    3721.20 [#/sec] (mean)
# Time per request:       268.731 [ms] (mean)
# Time per request:       0.269 [ms] (mean, across all concurrent requests)
# Transfer rate:          610.51 [Kbytes/sec] received
