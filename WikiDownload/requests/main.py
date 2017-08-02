#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python3
"""
Package  : WikiDownload - liaoxuefeng.com
Function : 下载liaoxuefeng.com上的文档
Author   : bihuchao <bihuchao1995@gmail.com>
"""

import os
import re
import pdfkit

if __name__ == "__main__":
    files = ["{0}.html".format(x) for x in range(1, 6)]
    pdfTitle = "Requests"
    options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
    try:
        # 不知道为什么会出现"raise IOError('wkhtmltopdf reported an error:\n' + stderr)"
        # 貌似不影响PDF生成，干脆屏蔽了
        pdfkit.from_file(files, pdfTitle + ".pdf", options=options)
    except IOError as e:
        print(e)
    
    #for file in files:
    #    os.remove(file)
    

    