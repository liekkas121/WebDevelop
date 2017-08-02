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
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

def getUrls(url):
    reponse = requests.get(url).text
    soup = BeautifulSoup(reponse, 'lxml')
    lis = soup.find_all('ul', {'class': "uk-nav uk-nav-side", 'style': "margin-right:-15px;"})[0].children
    urls = []
    for li in lis:
        if(li == "\n"):
            continue
        urls.append([li.a.string, "{0}{1}".format("https://www.liaoxuefeng.com", li.a['href'])])
    return urls

def getContent(url):
    global pngIndex
    global imgfiles

    reponse = requests.get(url).text
    soup = BeautifulSoup(reponse, 'lxml')
    div = str(soup.find('div', {'class' : "x-wiki-content x-main-content"}))
    
    imgs = re.findall(r'<img alt\=\".*?\" src\=\"(.*?)\"', div, re.S)
    for img in imgs:
        try:
            urlretrieve("http://www.liaoxuefeng.com"+img, "{0}.png".format(pngIndex))
            div = re.sub(r'<img alt\=\".*?\" src\=\"{0}\"'.format(img), "<img alt=\"1\" src=\"{0}.png\"".format(pngIndex), div)
            imgfiles.append("{0}.png".format(pngIndex))
            pngIndex += 1
        except:
            #f = open("1.txt", "w")
            #f.write(div)
            #f.close()
            print("BAD END")
            exit()
    
    
    return div
    
def htmlToPdf(files, pdfTitle):
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
    

def justDoIt(bookUrl):
    '''
    Function : 
    '''
    # Python 3
    global imgfiles
    global htmlTemplate
    urls = getUrls(bookUrl)
    files = []
    fileIndex = 1
    for url in urls:
        filename = "{0}.html".format(fileIndex)
        f = open(filename, "w", encoding="utf-8")
        f.write(htmlTemplate.format(div=getContent(url[1]), title=url[0]))
        f.close()
        print("{0} : {1}".format(fileIndex, url[0]))
        files.append(filename)
        fileIndex += 1
    # to PDF
    htmlToPdf(files, urls[0][0])
    
    for file in files:
        os.remove(file)
    for imgfile in imgfiles:
        os.remove(imgfile)
    

htmlTemplate = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body>
<div><center><h1>{title}</h1></center></div>
{div}
</body>
</html>
'''

pngIndex = 1
imgfiles = []

if __name__ == "__main__":
    #justDoIt("https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000")
    #justDoIt("https://www.liaoxuefeng.com/wiki/001434446689867b27157e896e74d51a89c25cc8b43bdb3000")
    #justDoIt("https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000")
    justDoIt("https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000")
    
    