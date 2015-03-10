#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Quantin Hsu'

import requests
from bs4 import BeautifulSoup
from Queue import Queue
import threading
import re
import time
import os

from login.WeiboLogin import WeiboLogin
import WeiboUser

# 存放用户信息和微博内容信息的目录
dirName = '/Users/quantin/data/weibo/01/'
startUrl = 'http://weibo.cn/1266321801'
# 用户信息文件
userFile = open(dirName + 'userinfo.txt', 'a+')
# 微博内容信息
contentFile = open(dirName + 'content.txt', 'a+')

cookies = {
        '_T_WM': '56ecedc3fa449397b30feee03a1b9d68',
        'SUB': '_2A255uo5FDeTxGeNK41oY8SfKzTyIHXVbRBINrDV6PUJbrdANLVHQkW2icuyOHeugE2jGfK7h8ktximDHiA..',
        'gsid_CTandWM': '4uwBb2141PYNuXKL9Me2An1UXaE',
        'M_WEIBOCN_PARAMS': 'rl%3D1'
    }

# cookies = {
#         '_T_WM': '909ee3fe2013318c183e41b479bda2af',
#         'SUB': '_2A255uhUtDeTxGeNK7VQR9CbMyDmIHXVbRLtlrDV6PUJbrdANLVDZkW0wgnNBemVIOTCKf6PQ4LyPm0dJqA..',
#         'gsid_CTandWM': '4utGb2141GxC4ZtsNszDxmVY40z',
#         'M_WEIBOCN_PARAMS': 'rl%3D1'
#     }

# cookies = {
#         '_T_WM': '811adfaa0430b74afd4f3bd75b85b635',
#         'SUB': '_2A255uh7bDeTxGeNK7VoR8SzNyzuIHXVbRKKTrDV6PUJbrdAKLUvFkW03yKW1XNQ_AzEEgP81TAqXBnhybQ..',
#         'gsid_CTandWM': '4uAnb2141oEWPnrVgdsaHmWtK1J',
#         'M_WEIBOCN_PARAMS': 'rl%3D1'
#     }

# cookies = {
#         '_T_WM': '1730741ece476736b119ce84cfc7f639',
#         'SUB': '_2A255ug0bDeTxGeNK7VUW-CnNwj-IHXVbRJNTrDV6PUJbrdAKLUPBkW1l1oSMls3Q8ssZg8wqnhZieTO8lw..',
#         'gsid_CTandWM': '4uHWb2141DdkRwcGJrD60mWq737',
#         'M_WEIBOCN_PARAMS': 'rl%3D1'
#     }

# 已经爬取的用户Id列表
alreadyCrawl = []

# 不活跃用户列表
notActiveUser = []

# 还未爬取的用户Id队列
readyToCrawl = Queue()

# postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}


# 没爬过的用户写入文件
def writeToFile(userId, userOtherInfo):
    try:
        #print weiboUser.userId + weiboUser.otherInfo
        userFile.write(userId + ' ' + userOtherInfo + ' ' + time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
        # crawlContent(userId)
        alreadyCrawl.append(userId)
    except:
        pass
    finally:
        userFile.flush()

def breadthFirstTraversal(weiboUser):
    pass

# 拿到cookies和起始url之后开始爬取
def startCrawl():
    for i in range(1, 1000):
        print 'i = %s' % str(i)

        if i % 20 == 0:
            time.sleep(20 * 60) # 休眠10分钟

        produceId = readyToCrawl.get()

        # 如果已经抓取了该用户，或者该用户为不活跃用户，则直接跳转
        if produceId in alreadyCrawl or produceId in notActiveUser:
            continue
        else:
            print produceId, '============'
            userOtherInfo, mcount, followsnum = WeiboUser.getUserInfoById(produceId, cookies)
            # 如果微博数小于100或者关注的人小于50则判定为不活跃用户
            if mcount < 100 or followsnum < 50:
                notActiveUser.append(produceId)
                continue
            else:
                writeToFile(produceId, userOtherInfo)
                WeiboUser.getUserContentById(produceId, cookies, contentFile)
                followsList = WeiboUser.getFollowsList(produceId, cookies)
                for iId in followsList:
                    # print iId
                    readyToCrawl.put(iId)

if __name__ == '__main__':
    # weiboLogin = WeiboLogin('18601346913', 'testsina')
    # weiboLogin = WeiboLogin('18373881@qq.com', 'testsina')
    # cookies = weiboLogin.getCookie()
    readyToCrawl.put('1266321801')
    startCrawl()

