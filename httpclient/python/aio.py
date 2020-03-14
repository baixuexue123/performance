#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import time
import httpx


urls = [
    'http://www.sohu.com',
    'http://www.sina.com',
    'http://www.qq.com/',
    'http://www.zhaopin.com/',
    'http://www.jd.com/',
    'http://www.zhibo8.cc/',
    'http://www.iqiyi.com/',
    'http://www.bootcss.com/',
    'http://www.redis.cn/',
    'http://cnodejs.org/',
    'http://bbs.tianya.cn/',
    'http://spark.apache.org/',
]

http_client = httpx.AsyncClient()


async def http_get(url):
    st = time.time()
    async with http_client as client:
        resp = await client.get(url, timeout=30)
    return url, resp, time.time() - st


def main():
    loop = asyncio.get_event_loop()
    tasks = [http_get(url) for url in urls]
    results = loop.run_until_complete(asyncio.gather(*tasks, loop=loop))
    total = 0
    for r in results:
        url, resp, t = r
        print(url, resp, t)
        total += t
    loop.close()
    return total


if __name__ == '__main__':
    st = time.time()
    print(main())
    print(time.time() - st)
