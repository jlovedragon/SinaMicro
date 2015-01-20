#/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Quantin Hsu'

import requests
from bs4 import BeautifulSoup

from login.WeiboLogin import WeiboLogin

class WeiboUser:
    'USER INFO'
    def __init__(self, id, otherInfo):
        self.id = id # 用户唯一id
        self.otherInfo = otherInfo
        # self.username = username # 姓名
        # self.urank = urank # 等级
        # self.sex = sex # 性别
        # self.address = address # 地址
        # self.mcount = mcount # 微博数
        # self.followsnum = followsnum # 关注人数
        # self.fansnum = fansnum # 粉丝人数

    def getUserInfo(self, userUrl, cookie):
        "Get UserInfo"
        respond = requests.get(userUrl, cookies=cookie)
        respond.encoding = 'utf-8'

        mainSoup = BeautifulSoup(respond.text, 'lxml')
        spaninfo = (mainSoup.find_all('span', 'ctt')[0]).text
        userinfo = spaninfo.encode('utf-8').strip().split(r' ')
        user = userinfo[0].replace('/', " ").replace('[在线]', '')
        idinfo = (mainSoup.find_all('img', 'por')[0])['src']
        self.id = idinfo[22:32].encode('utf-8')
        # 需要判断id是否已经读过
        mcountinfo = (mainSoup.find_all('span', 'tc')[0]).text
        mcount = mcountinfo[3:-1].encode('utf-8')
        followkey = '/' + self.id + '/' + 'follow'
        followsnuminfo = (mainSoup.find_all(attrs={"href": followkey})[0]).text
        followsnum = followsnuminfo[3:-1].encode('utf-8')
        fanskey = '/' + self.id + '/' + 'fans'
        fansnuminfo = (mainSoup.find_all(attrs={"href": fanskey})[0]).text
        fansnum = fansnuminfo[3:-1].encode('utf-8')
        self.otherInfo = user + ' ' + mcount + ' ' + followsnum + ' ' + fansnum
        print self.id + ' ' + self.otherInfo + '\n'
        return self.id, self.otherInfo

if __name__ == '__main__':
    weiboLogin = WeiboLogin('18601346913', 'testsina')
    cookie = weiboLogin.getCookie()
    weiboUser = WeiboUser(-1, -1)
    userId, userOtherInfo = weiboUser.getUserInfo('http://weibo.cn/hntv', cookie)
        