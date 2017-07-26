#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python3
"""
Package  : Python 3.* crawler
Function : Python 3.* 爬虫测试
Author   : bihuchao <bihuchao1995@gmail.com>
"""

import urllib.request
import urllib.parse

if __name__ == "__main__":
    # POST
    url = "http://localhost:88/server_crawler_test/main.php"
    data = {
        "username" : "毕沪超",
        "password" : "密码"
    }
    encode_data = urllib.parse.urlencode(data)
    headers = {}
    request = urllib.request.Request(url, encode_data.encode('utf-8'), headers)
    reponse = urllib.request.urlopen(request)
    print(reponse.read().decode('utf-8'))
    # GET
    url = "http://localhost:88/server_crawler_test/main.php?username=1&password=2"
    headers = {}
    request = urllib.request.Request(url, headers)
    reponse = urllib.request.urlopen(request)
    print(reponse.read().decode('utf-8'))
    
    