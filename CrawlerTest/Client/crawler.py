#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Package  : Crawler
Function : 爬虫 (适用于Python 2.* 和 Python 3.*)
Author   : bihuchao <bihuchao1995@gmail.com>
"""

import sys
if sys.version[0] == "2":
    from urllib2 import Request as Request
    from urllib2 import urlopen as Urlopen
    from urllib import urlencode as Urlencode
elif sys.version[0] == "3":
    from urllib.request import Request as Request
    from urllib.request import urlopen as Urlopen
    from urllib.parse import urlencode as Urlencode
else:
    print("Python Wrong Verison")
    exit()
    

if __name__ == "__main__":
    # POST
    url = "http://localhost:88/server_crawler_test/main.php"
    data = {
        "username" : "毕沪超",
        "password" : "密码"
    }
    headers = {}
    req = Request(url, Urlencode(data).encode('utf-8'), headers)
    rep = Urlopen(req)
    print(rep.read().decode('utf-8'))
    # GET
    url = "http://localhost:88/server_crawler_test/main.php?username=1&password=2"
    headers = {}
    req = Request(url, headers=headers)
    rep = Urlopen(req)
    print(rep.read().decode('utf-8'))
    
    
    
    
    
    