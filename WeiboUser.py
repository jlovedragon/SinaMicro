#/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Quantin Hsu'

import requests
from bs4 import BeautifulSoup
import json
import re
import time

from login.WeiboLogin import WeiboLogin

# # 存放文件目录
# dirName = '/Users/quantin/data/weibo/01/'

# # 用户微博内容文件
# contentFile = open(dirName + 'content.txt', 'a+')
# # 方便测试
# contentFile.write('==========================\n')
# contentFile.flush()

# cookies2 = {
#         '_T_WM': 'f584e482171b711253c08f1249e9cbf7',
#         'SUB': '_2A255u2d7DeTxGeNK41sV8yrJzDuIHXVbRAkzrDV6PUJbrdAKLWP3kW16jvnEn8V6p7GL_j0UMvVbvRpgkA..',
#         'gsid_CTandWM': '4uujb2141ZIHbyqx058WQn23g9j',
#         'M_WEIBOCN_PARAMS': 'rl%3D1'
#     }

postHeader = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'}

        # self.userId = userId # 用户唯一id
        # self.otherInfo = otherInfo
        # self.username = username # 姓名
        # self.urank = urank # 等级
        # self.sex = sex # 性别
        # self.address = address # 地址
        # self.mcount = mcount # 微博数
        # self.followsnum = followsnum # 关注人数
        # self.fansnum = fansnum # 粉丝人数

def getUserInfoById(userId, cookies):
    "Get UserInfo By Id"
    userUrl = 'http://weibo.cn/u/' + userId
    respond = requests.get(userUrl, cookies=cookies)
    respond.encoding = 'utf-8'
    
    mainSoup = BeautifulSoup(respond.text, 'lxml')
    spaninfo = (mainSoup.find_all('span', 'ctt')[0]).text
    userinfo = spaninfo.strip().split(' ')
    # print userinfo
    user = userinfo[0].encode('utf-8').replace('/', " ").replace('[在线]', '')
    mcountinfo = (mainSoup.find_all('span', 'tc')[0]).text
    mcount = mcountinfo[3:-1].encode('utf-8')
    followkey = '/' + userId + '/' + 'follow'
    followsnuminfo = (mainSoup.find_all(attrs={"href": followkey})[0]).text
    followsnum = followsnuminfo[3:-1].encode('utf-8')
    fanskey = '/' + userId + '/' + 'fans'
    fansnuminfo = (mainSoup.find_all(attrs={"href": fanskey})[0]).text
    fansnum = fansnuminfo[3:-1].encode('utf-8')
    otherInfo = user + ' ' + mcount + ' ' + followsnum + ' ' + fansnum
    print userId + ' ' + otherInfo + '\n'
    return otherInfo, int(mcount), int(followsnum)


def getUserInfoByUrl(userUrl, cookie):
    "Get UserInfo By Url"
    respond = requests.get(userUrl, cookies=cookie)
    respond.encoding = 'utf-8'
    
    mainSoup = BeautifulSoup(respond.text, 'lxml')
    spaninfo = (mainSoup.find_all('span', 'ctt')[0]).text
    userinfo = spaninfo.encode('utf-8').strip().split(r' ')
    user = userinfo[0].replace('/', " ")
    idinfo = (mainSoup.find_all('img', 'por')[0])['src']
    userId = idinfo[22:32].encode('utf-8')
    # 需要判断id是否已经读过
    mcountinfo = (mainSoup.find_all('span', 'tc')[0]).text
    mcount = mcountinfo[3:-1].encode('utf-8')
    followkey = '/' + userId + '/' + 'follow'
    followsnuminfo = (mainSoup.find_all(attrs={"href": followkey})[0]).text
    followsnum = followsnuminfo[3:-1].encode('utf-8')
    fanskey = '/' + userId + '/' + 'fans'
    fansnuminfo = (mainSoup.find_all(attrs={"href": fanskey})[0]).text
    fansnum = fansnuminfo[3:-1].encode('utf-8')
    otherInfo = user + ' ' + mcount + ' ' + followsnum + ' ' + fansnum
    print userId + ' ' + otherInfo + '\n'
    return userId, otherInfo

def getFollowsList(userId, cookies):
    pageNumUrl = 'http://weibo.cn/' + userId + '/follow?page='
    print pageNumUrl
    # cookies = {
    #     '_T_WM': '515f5aadd0e8442bbfdecda366865c64',
    #     'SUB': '_2A255uitADeTRGeNK41oY8SfKzTyIHXVbRLUIrDV6PUJbrdAKLVj8kW0BoVcsrxUUXy8DczIsfkA62-eWoQ..',
    #     'gsid_CTandWM': '4uwBb2141PYNuXKL9Me2An1UXaE',
    #     'M_WEIBOCN_PARAMS': 'rl%3D1'
    # }
    pageNumRespond = requests.get(pageNumUrl, cookies=cookies)
    pageNumRespond.encoding = 'utf-8'
    # print pageNumRespond.text
    followsList = []
    pageNumSoup = BeautifulSoup(pageNumRespond.text, 'lxml')
    postForm = (pageNumSoup.find_all(id='pagelist')[0]).text
    followPageNum = int(postForm[postForm.find('/')+1:-1])
    print followPageNum
    followTagPageOne = pageNumSoup.find_all(href=re.compile("http://weibo.cn/attention/add"))
    for fTagPageOne in followTagPageOne:
            fIdPageOne = fTagPageOne['href'][34:44]
            followsList.append(fIdPageOne)
    for i in range(2, followPageNum + 1):
        time.sleep(10)
        followsUrl = pageNumUrl + str(i)
        followsRespond = requests.get(followsUrl, cookies=cookies)
        followsRespond.encoding = 'utf-8'
        followSoup = BeautifulSoup(followsRespond.text, 'lxml')
        # 通过关注他拿到关注人的id
        # TODO：已经关注过了的人的拿不到id
        followTag = followSoup.find_all(href=re.compile("http://weibo.cn/attention/add"))
        for j,fTag in enumerate(followTag):
            fId = fTag['href'][34:44]
            # print fId
            followsList.append(fId)
    return followsList

def getUserContentById(userId, cookies, contentFile):
    "Get UserInfo By Id"
    userContentUrl = 'http://weibo.cn/u/' + userId + '?page='
    # 先解析第一页
    userRespPageOne = requests.get(userContentUrl, cookies=cookies)
    userRespPageOne.encoding = 'utf-8'
    
    userContentPageOneSoup = BeautifulSoup(userRespPageOne.text, 'lxml')
    contentTagPageOne = (userContentPageOneSoup.find_all(id=re.compile("M_")))
    for cTagPageOne in contentTagPageOne:
        contentFile.write(cTagPageOne.text.encode('utf-8') + '\n')
        contentFile.flush()
    for iPage in range(2, 3):
        time.sleep(10)
        contentUrl = userContentUrl + str(iPage)
        contentRespond = requests.get(contentUrl, cookies=cookies)
        contentRespond.encoding = 'utf-8'
        contentSoup = BeautifulSoup(contentRespond.text, 'lxml')
        contentTag = (contentSoup.find_all(id=re.compile("M_")))
        for cTag in contentTag:
            contentFile.write(cTag.text.encode('utf-8') + '\n')
            contentFile.flush()

if __name__ == '__main__':
    '''
    weiboLogin = WeiboLogin('18601346913', 'testsina')
    cookies = weiboLogin.getCookie()
    userOtherInfo = getUserInfoById('1266321801', cookies)
    getFollowsList('1266321801', cookies)
    '''
    # getUserContentById('1266321801', cookies2)
    # contentFile.close()

