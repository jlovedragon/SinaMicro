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

cookies = dict()

# 已经爬取的用户Id列表
alreadyCrawl = []

# 还未爬取的用户Id队列
readyToCrawl = Queue()

# postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}


# 没爬过的用户写入文件
def writeToFile(userId, userOtherInfo):
	try:
		#print weiboUser.userId + weiboUser.otherInfo
		userFile.write(userId + ' ' + userOtherInfo + ' ' + time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
		alreayCrawl.append(userId)
	except:
		pass
	finally:
		userFile.flush()

def breadthFirstTraversal(weiboUser):
	pass

# 拿到cookies和起始url之后开始爬取
def startCrawl():
	while 1:
		produceId = readyToCrawl.get()
		if produceId in alreadyCrawl:
			continue
		else:
			print produceId, '============'
			userOtherInfo, followsnum = WeiboUser.getUserInfoById(produceId, cookies)
			writeToFile(produceId, userOtherInfo)
			if int(followsnum) > 0:
				followsList = WeiboUser.getFollowsList(produceId, cookies)
				for iId in followsList:
					print iId
					readyToCrawl.put(iId)
		
	
if __name__ == '__main__':
	weiboLogin = WeiboLogin('18601346913', 'testsina')
	cookies = weiboLogin.getCookie()
	readyToCrawl.put('1266321801')
	startCrawl()
	




