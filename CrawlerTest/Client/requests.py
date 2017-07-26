#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python2
"""
Package  : Python 2.* crawler
Function : Python 2.* requests 爬虫测试
Author   : bihuchao <bihuchao1995@gmail.com>
"""

import requests

if __name__ == "__main__":
    # POST
    url = "http://localhost:88/server_crawler_test/main.php"
    
    data = {
        "username" : "毕沪超",
        "password" : "密码"
    }
    headers={}
    reponse = requests.post(url, data)
    print(reponse.text)
    # GET
    url = "http://localhost:88/server_crawler_test/main.php?name=1&password=1"
    
    reponse = requests.get(url)
    print(reponse.text)