#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python2
"""
Package  : 
Function : 
Author   : bihuchao <bihuchao1995@gmail.com>
"""

import os
import re
import pickle
import requests

def GetCourseDownUrl(url):
    global doneList
    if(re.findall(r'courseId\=([0-9]+)', url, re.S)[0] in [id for id in doneList]):
        print(u"已下载: {0}".format(doneList[re.findall(r'courseId\=([0-9]+)', url, re.S)[0]]))
        return 
    courseData = {}
    courseUrl = "http://study.163.com/dwr/call/plaincall/PlanNewBean.getPlanCourseDetail.dwr"
    coursePostData = {
        "scriptSessionId" :"", #"${scriptSessionId}190",
        "httpSessionId"   :"", #"3f1730f301c644a0887a1ce172019f96",
        "c0-param1"       :"", #"number:0",
        "c0-param2"       :"", #"null:null",
        "batchId"         :"1", # 任意数字 "1501511655976",
        "c0-id"           :"1", # 任意数字
        
        "callCount"       :"1",
        "c0-scriptName"   :"PlanNewBean",
        "c0-methodName"   :"getPlanCourseDetail",
        "c0-param0"       :"string:{0}".format(re.findall(r'courseId\=([0-9]+)', url, re.S)[0]),
    }
    headers = {}
    reponse = requests.post(courseUrl, data=coursePostData, headers = headers)
    ## 课程信息
    courseData['name'] = re.findall(r's0\.name\=\"(.*?)\"', reponse.text, re.S)[0].decode('unicode-escape')
    courseSectionNum = int(re.findall(r's0\.lessonsCount\=(.*?);', reponse.text, re.S)[0])
    
    if(os.path.exists("data/{0}.txt".format(courseData['name'].encode('gbk')))):
        print(courseSectionNum)
        print("Urls Exists!")
        #JustForWindows(courseData['name'])
        return courseData['name']
    courseData2 = re.findall(r'(s[0-9]+)\.lessonDtos\=(s[0-9]+);', reponse.text, re.S)
    courseData['ID'] = int(re.findall(r'{0}\.courseId\=(.*?);'.format(courseData2[0][0]), reponse.text, re.S)[0])
    courseData['chapterInfo'] = []
    print(u"课程名称：{0}".format(courseData['name']))
    ## 章
    chapterIndex = 1
    for subCourseData in courseData2:
        chapterInfo = {}
        chapterInfo['name'] = re.findall(r'{0}\.name=\"(.*?)\";'.format(subCourseData[0]), reponse.text, re.S)[0].decode('unicode-escape')
        chapterSectionNum = int(re.findall(r'{0}\.allCount=(.*?);'.format(subCourseData[0]), reponse.text, re.S)[0])
        sectionData = re.findall(r'{0}\[[0-9]+\]\=(s[0-9]+);'.format(subCourseData[1]), reponse.text, re.S)
        if(len(sectionData) != chapterSectionNum):
            print("Error : ChapterSectionNum")
        chapterInfo['ID'] = int(re.findall(r'{0}\.chapterId\=(.*?);'.format(sectionData[0]), reponse.text, re.S)[0])
        chapterInfo['sectionInfo'] = []
        print(u"{0} {1}".format(chapterIndex, chapterInfo['name']))
        ## 节
        sectionIndex = 1
        for subSection in sectionData:
            sectionInfo = {}
            sectionInfo['ID'] = int(re.findall(r'{0}\.id\=(.*?);'.format(subSection), reponse.text, re.S)[0])
            sectionInfo['name'] = re.findall(r'{0}\.lessonName\=\"(.*?)\";'.format(subSection), reponse.text, re.S)[0].decode('unicode-escape')
            ## video下载地址
            sectionUrl = "http://study.163.com/dwr/call/plaincall/LessonLearnBean.getVideoLearnInfo.dwr"
            sectionPostData = {
                "scriptSessionId" : "",   # "${scriptSessionId}190",
                "httpSessionId"   : "",   # "3f1730f301c644a0887a1ce172019f96",
                "batchId"         : "1",  # "1501511711444",
                "c0-id"           : "2",  # 任意数字
                
                "callCount"       : "1",
                "c0-scriptName"   : "LessonLearnBean",
                "c0-methodName"   : "getVideoLearnInfo",
                "c0-param0"       : "string:{0}".format(sectionInfo['ID']),
                "c0-param1"       : "string:{0}".format(courseData['ID']),
            }
            sectionReponse = requests.post(sectionUrl, data=sectionPostData, headers=headers)
            flvShdUrl = re.findall(r's1.flvShdUrl\=\"(.*?)\"', sectionReponse.text, re.S)
            if (len(flvShdUrl)):
                sectionInfo['downloadUrl'] = flvShdUrl[0]
            else:
                sectionInfo['downloadUrl'] = ""
                #print("Error : No flvShdUrl")
            # flvHdUrl  = re.findall(r's1.flvHdUrl\=\"(.*?)\"', sectionReponse.text, re.S)
            # flvSdUrl  = re.findall(r's1.flvSdUrl\=\"(.*?)\"', sectionReponse.text, re.S)[0]
            # flvShdUrl = re.findall(r's1.flvShdUrl\=\"(.*?)\"', sectionReponse.text, re.S)[0]
            # mp4HdUrl  = re.findall(r's1.mp4HdUrl\=\"(.*?)\"', sectionReponse.text, re.S)[0]
            # mp4SdUrl  = re.findall(r's1.mp4SdUrl\=\"(.*?)\"', sectionReponse.text, re.S)[0]
            # mp4ShdUrl = re.findall(r's1.mp4ShdUrl\=\"(.*?)\"', sectionReponse.text, re.S)[0]
            print(u"    {0}.{1} {2}".format(chapterIndex, sectionIndex, sectionInfo['name']))
            chapterInfo['sectionInfo'].append(sectionInfo)
            sectionIndex += 1
        courseData['chapterInfo'].append(chapterInfo)
        chapterIndex += 1
    
    #print(courseData['name'])
    #print(courseData['ID'])
    #print(courseData['chapterInfo'][0]['name'])
    #print(courseData['chapterInfo'][0]['ID'])
    #print(courseData['chapterInfo'][0]['sectionInfo'][0]['name'])
    #print(courseData['chapterInfo'][0]['sectionInfo'][0]['ID'])
    #print(courseData['chapterInfo'][0]['sectionInfo'][0]['downloadUrl'])
    
    data = []
    for rawData in courseData['chapterInfo']:
        sectionName = []
        sectionUrls = []
        for rawData2 in rawData['sectionInfo']:
            sectionName.append(rawData2['name'])
            if(rawData2['downloadUrl']):
                sectionUrls.append([rawData2['downloadUrl']])
            else:
                sectionUrls.append([])
        data.append([rawData['name'], sectionName, sectionUrls])
    
    pickle.dump(data, open('data/{0}.txt'.format(courseData['name'].encode('gbk')), 'wb'))
    
    print(courseSectionNum)
    
    return courseData['name']

# 视频格式
# chapterName
# sectionName
# sectionUrls
# 文件名处理
def JustForWindows(courseName):
    '''
    Function : 将视频Url转为windows下使用的格式
    '''
    if not courseName:
        return 
    data = pickle.load(open('data/{0}.txt'.format(courseName.encode('gbk')), 'rb'))
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
                videoFormat = re.findall(r'\.([a-z0-9][a-z0-9][a-z0-9])\?', url, re.S)[0]
                f2.write(url+"\n")
                if(urlIndex):
                    f.write("move {0} \"{1}/{2} {3}.{4}\"\n".format(re.findall(r'\/([^/]+.{0})\?'.format(videoFormat), url, re.S)[0], subData[0].encode('gbk'), subData[1][lessonIndex].strip(" ").encode('gbk'), urlIndex+1, videoFormat))
                else:
                    f.write("move {0} \"{1}/{2}.{3}\"\n".format(re.findall(r'\/([^/]+.{0})\?'.format(videoFormat), url, re.S)[0], subData[0].encode('gbk'), subData[1][lessonIndex].strip(" ").encode('gbk'), videoFormat))
                urlIndex += 1
        chapterIndex += 1
    f.close()
    f2.close()
    
    return 


if __name__ == "__main__":
    # 已下载
    doneList = {
        #
    }
    # HTTP
    courseName = GetCourseDownUrl("http://study.163.com/course/introduction.htm?courseId=1008001")
    
    JustForWindows(courseName)
    
    