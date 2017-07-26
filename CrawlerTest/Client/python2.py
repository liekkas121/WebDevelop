#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python3
"""
Package  : Python 2.* crawler
Function : Python 2.* 爬虫测试
Author   : bihuchao <bihuchao1995@gmail.com>
"""

import urllib
import urllib2

if __name__ == "__main__":
    # POST
    url = "http://localhost:88/server_crawler_test/main.php"
    data = {
        "username" : "毕沪超",
        "password" : "密码"
    }
    encode_data = urllib.urlencode(data)
    headers = {}
    request = urllib2.Request(url, encode_data.encode('utf-8'), headers)
    reponse = urllib2.urlopen(request)
    print(reponse.read().decode('utf-8'))
    # GET
    url = "http://localhost:88/server_crawler_test/main.php?username=1&password=2"
    headers = {}
    request = urllib2.Request(url=url, data=None, headers=headers)
    reponse = urllib2.urlopen(request)
    print(reponse.read().decode('utf-8'))
    
    