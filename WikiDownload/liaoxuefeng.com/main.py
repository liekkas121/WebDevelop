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
import time
import pdfkit
import hashlib
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()
import threading
import multiprocessing


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

def GetChapterContent2(chapterIndex, chapterItem):
    imgFiles = []
    while(True):
        try:
            soup = BeautifulSoup(requests.get(chapterItem['url'], verify=False).text, 'lxml')
            div = str(soup.find('div', {'class' : "x-wiki-content x-main-content"}))
            
            imgs = re.findall(r'<img alt\=\".*?\" src\=\"(.*?)\"', div, re.S)
            
            for img in imgs:
                imgData = requests.get("http://www.liaoxuefeng.com"+img, verify=False).content
                imgFilename = hashlib.md5(imgData).hexdigest()+".png"
                with open(imgFilename, "wb") as f:
                    f.write(imgData)
                div = re.sub(r'<img alt\=\".*?\" src\=\"{0}\"'.format(img), "<img alt=\"1\" src=\"{0}\"".format(imgFilename), div)
                imgFiles.append(imgFilename)
            with open("{0}.html".format(chapterIndex), "w", encoding='utf-8') as f:
                f.write(htmlTemplate.format(div=div, title=chapterItem['title']))
            
            return imgFiles
        except:
            print("Error : {0}".format(chapterIndex))

class LiaoxuefengWikiDownload(object):
    
    def __init__(self, wikiUrl, pdfFilename):
        self.wikiUrl = wikiUrl
        self.pdfFilename = pdfFilename
        self.session = requests.Session()
        self.session.verify = False
    
    def GetChapterInfo(self):
        soup = BeautifulSoup(self.session.get(self.wikiUrl).text, 'lxml')
        
        return [{'title':item.find('a').text, 'url':"https://www.liaoxuefeng.com"+item.find('a')['href']} for item in soup.find('ul', {'class': "uk-nav uk-nav-side", 'style': "margin-right:-15px;"}).find_all('li')]
    
    def GetChapterContent(self, chapterIndex, chapterItem):
        imgFiles = []
        while(True):
            try:
                soup = BeautifulSoup(self.session.get(chapterItem['url']).text, 'lxml')
                div = str(soup.find('div', {'class' : "x-wiki-content x-main-content"}))
                
                imgs = re.findall(r'<img alt\=\".*?\" src\=\"(.*?)\"', div, re.S)
                
                for img in imgs:
                    imgData = self.session.get("http://www.liaoxuefeng.com"+img).content
                    imgFilename = hashlib.md5(imgData).hexdigest()+".png"
                    with open(imgFilename, "wb") as f:
                        f.write(imgData)
                    div = re.sub(r'<img alt\=\".*?\" src\=\"{0}\"'.format(img), "<img alt=\"1\" src=\"{0}\"".format(imgFilename), div)
                    imgFiles.append(imgFilename)
                with open("{0}.html".format(chapterIndex), "w", encoding='utf-8') as f:
                    f.write(htmlTemplate.format(div=div, title=chapterItem['title']))
                
                return imgFiles
            except:
                print("Error : {0}".format(chapterIndex))
            
    def HTMLToPdf(self, files, pdfFilename):
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
            pdfkit.from_file(files, pdfFilename + ".pdf", options=options)
        except IOError as e:
            #print(e)
            pass
    
    def run(self, process_num=1):
        imgFiles = []
        
        chapterInfo = self.GetChapterInfo()
        htmlFiles = ["{0}.html".format(i) for i in range(len(chapterInfo))]
        
        # Single-Thread
        if process_num == 1:
            startTimestamp = time.time()
            for chapterIndex, chapterItem in enumerate(chapterInfo):
                result = self.GetChapterContent(chapterIndex, chapterItem)
                imgFiles += result
        # Multi-Process
        else:
            pool = multiprocessing.Pool(process_num)
            processTasks = []
            for chapterIndex, chapterItem in enumerate(chapterInfo):
                processTasks.append(pool.apply_async(func=GetChapterContent2, args=(chapterIndex, chapterItem, )))
            startTimestamp = time.time()
            pool.close()
            pool.join()
            for process in processTasks:
                imgFiles += process.get()
        print("Download : {0} s".format(time.time()-startTimestamp))
        
        self.HTMLToPdf(htmlFiles, self.pdfFilename)
        
        # 将下面写成列表表达式不可以。
        for item in imgFiles+htmlFiles:
            if(os.path.isfile(item)):
                os.remove(item)

if __name__ == "__main__":
    wikis = [
        ["https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000", "Python3教程"],
        ["https://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000", "Python2.7教程"],
        ["https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000", "Git教程"],
        ["https://www.liaoxuefeng.com/wiki/001434446689867b27157e896e74d51a89c25cc8b43bdb3000", "JavaScript教程"],
    ]
    for wiki in wikis:
        LiaoxuefengWikiDownload(wiki[0], wiki[1]).run(process_num=1)
    
    
    