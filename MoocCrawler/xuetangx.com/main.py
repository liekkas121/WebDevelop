#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python3
"""
Package  : MOOC视频下载-学堂在线 
Function : 
Author   : bihuchao <bihuchao1995@gmail.com>
"""

import json
import requests
import re
import pickle
from bs4 import BeautifulSoup

def GetCookieFromFile(cookieFile):
    '''
    Function : 从文件中获取Cookie
    '''
    f = open(cookieFile, "r")
    cookieRaw = json.loads(f.read())
    f.close()
    cookie = {}
    for cookieDict in cookieRaw:
        cookie[cookieDict['name']] = cookieDict['value']
    
    return cookie
    
def Cookie2Str(cookie):
    '''
    Function : cookie转str
    '''
    
    str = ""
    for key in cookie:
        str += "{0}={1}; ".format(key, cookie[key])    
    
    return str[:-2]

if __name__ == "__main__":
    
    courseUrl = "http://www.xuetangx.com/courses/course-v1:TsinghuaX+80000901X_p1+sp/courseware/d9f8095797484b96a2df7a5850fed593/"
    headers = {}
    headers['Cookie'] = Cookie2Str(GetCookieFromFile("export.json"))
    reponse = requests.get(courseUrl, headers=headers)
    soup = BeautifulSoup(reponse.text, 'lxml')
    navRawData = soup.find('nav', {'aria-label':"课程导航"})
    data = []
    chapterIndex = 0
    for chapterRawData in navRawData.find_all('div'):
        chapterName = chapterRawData.find('h3').find('a').string.strip()
        print("{0} {1}".format(chapterIndex, chapterName.encode('gbk')))
        chapterData = [liRawData.find('a')['href'] for liRawData in chapterRawData.find('ul').find_all('li')]
        lessonName = [liRawData.find('a').find('p').string for liRawData in chapterRawData.find('ul').find_all('li')]
        lessonDownUrl = []
        lessonIndex = 0
        for lesson in chapterData:
            reponse = requests.get("http://www.xuetangx.com" + lesson, headers=headers)
            tempUrl = []
            lessonUrls = re.findall(r'data-ccsource=&#39;(.*?)&', reponse.text, re.S)
            for lessonUrl in lessonUrls:
                reponse = requests.get("http://www.xuetangx.com/videoid2source/"+lessonUrl, headers=headers)
                tempUrl.append(json.loads(reponse.text)['sources']['quality20'][0])
            lessonDownUrl.append(tempUrl)
            print("    {0}.{1} {2} {3}".format(chapterIndex, lessonIndex, lessonName[lessonIndex].encode('gbk'), len(tempUrl)))
            lessonIndex += 1
        chapterIndex += 1
        data.append([chapterName, lessonName, lessonDownUrl])
    
    pickle.dump(data, open('tmp.txt', 'wb'))
    
    #data = pickle.load(open('tmp.txt', 'rb'))
    f = open("main.bat", "w")
    f2 = open("main.txt", "w")
    f.write(": created by python\n")
    chapterIndex = 0
    for subData in data:
        f.write(": {0} {1}\n".format(chapterIndex+1, subData[0].encode('gbk')))
        f.write("mkdir \"{0}\"\n".format(subData[0].encode('gbk')))
        for lessonIndex in range(0, len(subData[1])):
            urlIndex = 0
            for url in subData[2][lessonIndex]:
                f2.write(url+"\n")
                if(urlIndex):
                    f.write("move {0} \"{1}/{2} {3}.mp4\"\n".format(re.findall(r'com\/(.*?.mp4)\?', url, re.S)[0], subData[0].encode('gbk'), subData[1][lessonIndex].strip(" ").encode('gbk'), urlIndex+1))
                else:
                    f.write("move {0} \"{1}/{2}.mp4\"\n".format(re.findall(r'com\/(.*?.mp4)\?', url, re.S)[0], subData[0].encode('gbk'), subData[1][lessonIndex].strip(" ").encode('gbk')))
                urlIndex += 1
        chapterIndex += 1
    f.close()
    f2.close()
    
    
    print("END")