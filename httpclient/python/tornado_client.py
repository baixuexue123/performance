#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient


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

http_client = AsyncHTTPClient()


async def http_get(url):
    st = time.time()
    resp = await http_client.fetch(url)
    return url, resp, time.time() - st


async def main():
    tasks = [http_get(url) for url in urls]
    total = 0
    for url, resp, t in await gen.multi(tasks):
        print(url, resp, t)
        total += t
    return total


if __name__ == '__main__':
    st = time.time()
    print(IOLoop.current().run_sync(main))
    print(time.time() - st)
