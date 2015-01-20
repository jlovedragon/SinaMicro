#/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Quantin Hsu'

import requests
from bs4 import BeautifulSoup
import json
import re

from login.WeiboLogin import WeiboLogin

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
    return otherInfo, followsnum


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
    #     '_T_WM': '26a84199a1c84735dc3079aef4a95a1b',
    #     'SUB': '_2A255ucYrDeTxGeNK7VUW-CnNwj-IHXVbRepjrDV6PUJbrdAKLWTbkW2C1UECqjaZCaYkkeZFTLBK9pQxJg..',
    #     'gsid_CTandWM': '4uG9b2141YTtjaGftAPMDmWq737',
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
    for i in range(1, followPageNum + 1):
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


if __name__ == '__main__':
    weiboLogin = WeiboLogin('18601346913', 'testsina')
    cookies = weiboLogin.getCookie()
    userOtherInfo = getUserInfoById('1266321801', cookies)
    getFollowsList('1266321801', cookies)
        