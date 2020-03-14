#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gevent
import gevent.monkey; gevent.monkey.patch_socket()

import time
import requests

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


def http_get(url):
    st = time.time()
    resp = requests.get(url)
    return url, resp, time.time() - st


def main():
    threads = []
    for url in urls:
        threads.append(gevent.spawn(http_get, url))
    total = 0
    for t in gevent.joinall(threads):
        url, resp, t = t.get()
        print(url, resp, t)
        total += t
    return total


if __name__ == '__main__':
    st = time.time()
    print(main())
    print(time.time() - st)
