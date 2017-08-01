#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python3
"""
Package  : MOOCDownload - icourse163.org 
Function : 
Author   : bihuchao <bihuchao1995@gmail.com>
"""

import re
import os
import json
import pickle
import requests
from bs4 import BeautifulSoup

def GetCourseDownUrl(courseUrl):
    '''
    Function : 
    '''
    # 数据结构
    '''
    数据结构
    courseName
    courseId
    chapterInfo
    [
        chapterName
        sectionInfo
        [
            sectionName
            lessonInfo
            [
                lessonName
                lessonId
                lessonContentId
                lseeonUrls
            ]
        ]
    ]
    '''
    courseData = {}
    # courseName
    courseNameRawDataSoup = BeautifulSoup(requests.get(courseUrl, headers={}).text, 'lxml')
    courseData['courseName'] = courseNameRawDataSoup.find('h4').string
    if(os.path.exists("data/{0}.txt".format(courseData['courseName']))):
        print("Urls Exists!")
        return courseData['courseName']
    # courseId
    courseData['courseId'] = re.findall(r'tid\=([0-9]+)', courseUrl, re.S)[0]
    # chapterInfo
    courseData['chapterInfo'] = []
    url = "http://www.icourse163.org/dwr/call/plaincall/CourseBean.getLastLearnedMocTermDto.dwr"
    data = {
        'callCount'       : "1",
        'scriptSessionId' : "${scriptSessionId}190",
        'httpSessionId'   : "8c0b2fb91e7343648950e9dcdaf8db43",
        'c0-scriptName'   : "CourseBean",
        'c0-methodName'   : "getLastLearnedMocTermDto",
        'c0-id'           : "0",
        'c0-param0'       : "number:{0}".format(courseData['courseId']),
        'batchId'         : "1501600602054",
    }
    headers = {
        'Cookie': 'NTESSTUDYSI=8c0b2fb91e7343648950e9dcdaf8db43; EDUWEBDEVICE=20bb0f1b7543406a8ab1b1e4de3368f0; __urscj_=1; STUDY_SESS="5J8xUQeE3G0aR0xJ5CpDOAyM8Wx5prU/rbgRgC9STZHKxvoevhbfuOIxdEzmwJCecRFmeR3rbdtMokRn0Pjt9IkteDxUxlzLHiHP7XAtnP19aRfdTWaHRbNNkMuhQDUq29HdC8bAdnJ4fxx3qSNX22BVWKrgcH2aFSmUjpPUoBo="; STUDY_INFO=971724|30|7626860|1501588512598; NETEASE_WDA_UID=7626860#|#1435389712724; utm="eyJ0IjoiIiwicyI6IiIsImMiOiIiLCJtIjoiIiwiY3QiOiIiLCJpIjoiIn0=|"; __utma=63145271.936852798.1501556108.1501597868.1501600158.3; __utmb=63145271.15.9.1501600630599; __utmc=63145271; __utmz=63145271.1501556108.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    }
    reponse = requests.post(url, data=data, headers=headers)
    chapterIndex = 1
    for chapterTag in re.findall(r's1\[[0-9]+\]\=(s[0-9]+);', reponse.text, re.S):
        chapterData = {}
        # chapterName
        chapterData['chapterName'] = re.findall(r'{0}\.name\=\"(.*?)\";'.format(chapterTag), reponse.text, re.S)[0]
        print("{1} {0}".format(chapterData['chapterName'].encode('latin-1').decode('unicode_escape'), chapterIndex))
        # sectionInfo
        chapterData['sectionInfo'] = []
        chapterTag2 = re.findall(r'{0}\.lessons\=(.*?);'.format(chapterTag), reponse.text, re.S)[0]
        sectionIndex = 1
        for sectionTag in re.findall(r'{0}\[[0-9]+\]\=(s[0-9]+);'.format(chapterTag2), reponse.text, re.S):
            sectionData = {}
            # sectionName
            sectionData['sectionName'] = re.findall(r'{0}\.name\=\"(.*?)\";'.format(sectionTag), reponse.text, re.S)[0]
            sectionTag2 = re.findall(r'{0}\.units\=(.*?);'.format(sectionTag), reponse.text, re.S)[0]
            # lessonInfo
            sectionData['lessonInfo'] = []
            print("    {1}.{2} {0}".format(sectionData['sectionName'].encode('latin-1').decode('unicode_escape'), chapterIndex, sectionIndex))
            lessonIndex = 1
            for lessonTag in re.findall(r'{0}\[[0-9]+\]\=(s[0-9]+);'.format(sectionTag2), reponse.text, re.S):
                lessonData = {}
                # lessonName
                lessonData['lessonName'] = re.findall(r'{0}\.name\=\"(.*?)\";'.format(lessonTag), reponse.text, re.S)[0]
                # lessonId
                lessonData['lessonId'] = re.findall(r'{0}\.id\=(.*?);'.format(lessonTag), reponse.text, re.S)[0]
                # lessonContentId
                lessonData['lessonContentId'] = re.findall(r'{0}\.contentId\=(.*?);'.format(lessonTag), reponse.text, re.S)[0]
                # lseeonUrl
                url = "http://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr"
                data = {
                    'callCount'       : '1',
                    'scriptSessionId' : '${scriptSessionId}190',
                    'httpSessionId'   : '8c0b2fb91e7343648950e9dcdaf8db43',
                    'c0-scriptName'   : 'CourseBean',
                    'c0-methodName'   : 'getLessonUnitLearnVo',
                    'c0-id'           : '0',
                    'c0-param0'       : 'number:{0}'.format(lessonData['lessonContentId']),
                    'c0-param1'       : 'number:1',
                    'c0-param2'       : 'number:0',
                    'c0-param3'       : 'number:{0}'.format(lessonData['lessonId']),
                    'batchId'         : '1501608211644'
                }
                reponse2 = requests.post(url, data=data)
                try:
                    lessonData['lessonUrl'] = re.findall(r's0.flvShdUrl\=\"(.*?)\"', reponse2.text, re.S)[0]
                except:
                    lessonData['lessonUrl'] = ""
                # flvHdUrl  = re.findall(r's1.flvHdUrl\=\"(.*?)\"', sectionReponse.text, re.S)
                # flvSdUrl  = re.findall(r's1.flvSdUrl\=\"(.*?)\"', sectionReponse.text, re.S)[0]
                # flvShdUrl = re.findall(r's1.flvShdUrl\=\"(.*?)\"', sectionReponse.text, re.S)[0]
                # mp4HdUrl  = re.findall(r's1.mp4HdUrl\=\"(.*?)\"', sectionReponse.text, re.S)[0]
                # mp4SdUrl  = re.findall(r's1.mp4SdUrl\=\"(.*?)\"', sectionReponse.text, re.S)[0]
                # mp4ShdUrl = re.findall(r's1.mp4ShdUrl\=\"(.*?)\"', sectionReponse.text, re.S)[0]
                print("        {1}.{2}.{3} {0}".format(lessonData['lessonName'].encode('latin-1').decode('unicode_escape'), chapterIndex, sectionIndex, lessonIndex))
                sectionData['lessonInfo'].append(lessonData)
                lessonIndex += 1
            chapterData['sectionInfo'].append(sectionData)
            sectionIndex += 1
        courseData['chapterInfo'].append(chapterData)
        chapterIndex += 1
    json.dump(courseData, open('data\{0}.txt'.format(courseData['courseName']), "w"))
    
    return courseData['courseName']
    
def JustForWindows(courseName):
    if not courseName:
        return 
    courseData = json.load(open('data\{0}.txt'.format(courseName), "r"))
    f = open("main.bat", "w")
    f2 = open("main.txt", "w")
    f.write(": created by python\n")
    chapterIndex = 0
    for chapterData in courseData['chapterInfo']:
        f.write(": {0} {1}\n".format(chapterIndex+1, chapterData['chapterName'].encode('latin-1').decode('unicode_escape')))
        f.write("mkdir \"{0} {1}\"\n".format(chapterIndex+1, chapterData['chapterName'].encode('latin-1').decode('unicode_escape')))
        sectionIndex = 0
        for sectionData in chapterData['sectionInfo']:
            f.write(": {0}.{1} {2}\n".format(chapterIndex+1, sectionIndex+1, sectionData['sectionName'].encode('latin-1').decode('unicode_escape')))
            f.write("mkdir \"{0} {1}/{2} {3}\"\n".format(chapterIndex+1, chapterData['chapterName'].encode('latin-1').decode('unicode_escape'), sectionIndex+1, sectionData['sectionName'].encode('latin-1').decode('unicode_escape')))
            lessonIndex = 0
            for lessonData in sectionData['lessonInfo']:
                #print(lessonData['lessonUrl'])
                #exit()
                #
                #videoFormat = "flv"
                if(lessonData['lessonUrl'] != ""):
                    videoFormat = re.findall(r'\.([a-z][a-z][a-z])\?', lessonData['lessonUrl'], re.S)[0]
                    temp0 = re.findall(r'\/([^/]+.{0})\?'.format(videoFormat), lessonData['lessonUrl'], re.S)[0]
                    temp1 = chapterIndex+1
                    temp2 = chapterData['chapterName'].encode('latin-1').decode('unicode_escape')
                    temp3 = sectionIndex+1
                    temp4 = sectionData['sectionName'].encode('latin-1').decode('unicode_escape')
                    temp5 = lessonIndex+1
                    temp6 = lessonData['lessonName'].encode('latin-1').decode('unicode_escape')
                    temp7 = videoFormat
                    f.write("move {0} \"{1} {2}/{3} {4}/{5} {6}.{7}\"\n".format(temp0, temp1, temp2, temp3, temp4, temp5, temp6, temp7))
                    f2.write(lessonData['lessonUrl']+"\n")
                lessonIndex += 1
            sectionIndex += 1
        chapterIndex += 1
    f.close()
    f2.close()
    
    
    return

if __name__ == "__main__":
    courseName = GetCourseDownUrl("http://www.icourse163.org/learn/BIT-1001870001?tid=1001962001")
    JustForWindows(courseName)
    
    
            
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    