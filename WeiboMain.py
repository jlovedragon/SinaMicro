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

# 存放用户信息和微博信息
dirName = '/Users/quantin/data/weibo/'
startUrl = 'http://weibo.cn/yaochen'
# 用户信息文件
userFile = open(dirName + 'userinfo.txt', 'a+')

# 已经爬取的用户Id列表
alreadyCrawl = []

# 还未爬取的用户Id队列
readyToCrawl = Quene()

# postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}


# 没爬过的用户写入文件
def writeToFile(weiboUser):
	if weiboUser.userId in alreadyCrawl:
		print 'haved!!!!!'
		return
	else:
		#print weiboUser.userId + weiboUser.otherInfo
		userFile.write(weiboUser.userId + ' ' + weiboUser.otherInfo + ' ' + time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
		alreayCrawl.append(weiboUser.userId)

def breadthFirstTraversal(weiboUser):
	readyToCrawl.append(weiboUser.userId)
	weiboUser.getFollowsList(cookies)


# 拿到cookies和起始url之后开始爬取
def startCrawl(originUrl, cookies):
	weiboUser = WeiboUser.WeiboUser(-1)
	weiboUser.getUserInfo('http://weibo.cn/yaochen', cookies)

	breadthFirstTraversal(weiboUser)

if __name__ == '__main__':
	weiboLogin = WeiboLogin('18601346913', 'testsina')
	cookies = weiboLogin.getCookie()
	startCrawl('http://weibo.cn/yaochen', cookies)
	




