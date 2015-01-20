#/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Quantin Hsu'

import requests
from bs4 import BeautifulSoup
import json
import re

from login.WeiboLogin import WeiboLogin

postHeader = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'}

class WeiboUser:
    'USER INFO'
    def __init__(self, id):
        self.id = id # 用户唯一id
        # self.otherInfo = otherInfo
        # self.username = username # 姓名
        # self.urank = urank # 等级
        # self.sex = sex # 性别
        # self.address = address # 地址
        # self.mcount = mcount # 微博数
        # self.followsnum = followsnum # 关注人数
        # self.fansnum = fansnum # 粉丝人数

    def getUserInfo(self, userUrl, cookie):
        "Get UserInfo"
        respond = requests.get(userUrl, data=postHeader, cookies=cookie)
        respond.encoding = 'utf-8'
        
        mainSoup = BeautifulSoup(respond.text, 'lxml')
        spaninfo = (mainSoup.find_all('span', 'ctt')[0]).text
        userinfo = spaninfo.encode('utf-8').strip().split(r' ')
        user = userinfo[0].replace('/', " ")
        idinfo = (mainSoup.find_all('img', 'por')[0])['src']
        self.id = idinfo[22:32].encode('utf-8')
        # 需要判断id是否已经读过
        mcountinfo = (mainSoup.find_all('span', 'tc')[0]).text
        mcount = mcountinfo[3:-1].encode('utf-8')
        followkey = '/' + self.id + '/' + 'follow'
        followsnuminfo = (mainSoup.find_all(attrs={"href": followkey})[0]).text
        self.followsnum = followsnuminfo[3:-1].encode('utf-8')
        fanskey = '/' + self.id + '/' + 'fans'
        fansnuminfo = (mainSoup.find_all(attrs={"href": fanskey})[0]).text
        fansnum = fansnuminfo[3:-1].encode('utf-8')
        self.otherInfo = user + ' ' + mcount + ' ' + self.followsnum + ' ' + fansnum
        print self.id + ' ' + self.otherInfo + '\n'
        return self.id, self.otherInfo

    def getFollowsList(self, cookies):
        self.pageNumUrl = 'http://weibo.cn/' + self.id + '/follow?page='
        print self.pageNumUrl
        # cookies = {
        #     '_T_WM': '26a84199a1c84735dc3079aef4a95a1b',
        #     'SUB': '_2A255ucYrDeTxGeNK7VUW-CnNwj-IHXVbRepjrDV6PUJbrdAKLWTbkW2C1UECqjaZCaYkkeZFTLBK9pQxJg..',
        #     'gsid_CTandWM': '4uG9b2141YTtjaGftAPMDmWq737',
        #     'M_WEIBOCN_PARAMS': 'rl%3D1'
        # }
        pageNumRespond = requests.get(self.pageNumUrl, cookies=cookies)
        pageNumRespond.encoding = 'utf-8'
        # print pageNumRespond.text

        self.followsIdList = []
        pageNumSoup = BeautifulSoup(pageNumRespond.text, 'lxml')
        postForm = (pageNumSoup.find_all(id='pagelist')[0]).text
        followPageNum = int(postForm[-3:-1])
        print followPageNum

        for i in range(1, followPageNum + 1):
            followsUrl = self.pageNumUrl + str(i)
            followsRespond = requests.get(followsUrl, cookies=cookies)
            followsRespond.encoding = 'utf-8'

            followSoup = BeautifulSoup(followsRespond.text, 'lxml')
            # 通过关注他拿到关注人的id
            # TODO：已经关注过了的人的拿不到id
            followTag = followSoup.find_all(href=re.compile("http://weibo.cn/attention/add"))
            for j,fTag in enumerate(followTag):
                fId = fTag['href'][35:44]
                self.followsIdList.append(fId)


if __name__ == '__main__':
    weiboLogin = WeiboLogin('18601346913', 'testsina')
    cookies = weiboLogin.getCookie()
    weiboUser = WeiboUser(-1)
    userId, userOtherInfo = weiboUser.getUserInfo('http://weibo.cn/yaochen', cookies)
    weiboUser.getFollowsList(cookies)
        