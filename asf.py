#!/usr/bin/env python
# encoding: utf-8

"""
@author: paul.xie
@software: PyCharm
@time: 2017/1/10 12:35
"""

import requests

cookies = {
    'PHPSESSID': '6ae9hlk3ipf4fg3vpjh0t1tu12',
    'guideState': '1',
    'cid': '6ae9hlk3ipf4fg3vpjh0t1tu121484015615',
    'ComputerID': '6ae9hlk3ipf4fg3vpjh0t1tu12170110+103335',
}

headers = {
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'http://www.iwencai.com/stockpick/',
    'X-Requested-With': 'XMLHttpRequest',
    'Proxy-Connection': 'keep-alive',
}

print requests.get('http://www.iwencai.com/stockpick/query-hint-list?sessionId=355171484022909644&q=%E8%82%A1%E7%A5%A8', headers=headers, cookies=cookies).json()