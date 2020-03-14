#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


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
    total = 0
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = [executor.submit(http_get, url) for url in urls]
        for future in as_completed(futures):
            url, resp, t = future.result()
            print(url, resp, t)
            total += t
    return total


if __name__ == '__main__':
    st = time.time()
    print(main())
    print(time.time() - st)
