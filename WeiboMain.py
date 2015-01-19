#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import time
import os

from login.WeiboLogin import WeiboLogin

dirName = '/home/quentin/data/weibo/'
startUrl = 'http://weibo.cn/hntv'
userFile = open(dirName + 'userinfo.txt', 'a+')
postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}

weiboLogin = WeiboLogin('18601346913', 'testsina')
cookie = weiboLogin.getCookie()
#respond = requests.post(startUrl, data=postHeader, cookies=cookie)
respond = requests.post(startUrl, cookies=cookie)
respond.encoding = 'utf-8'
#print respond.text

soup = BeautifulSoup(respond.text, 'lxml')
spaninfo = (soup.find_all('span', 'ctt')[0]).text
userinfo = spaninfo.encode('utf-8').strip().split(r' ')
user = userinfo[0].replace('/', " ")
idinfo = (soup.find_all('img', 'por')[0])['src']
id = idinfo[22:32].encode('utf-8')
mcountinfo = (soup.find_all('span', 'tc')[0]).text
mcount = mcountinfo[3:-1].encode('utf-8')
followkey = '/' + id + '/' + 'follow'
followsnuminfo = (soup.find_all(attrs={"href": followkey})[0]).text
followsnum = followsnuminfo[3:-1].encode('utf-8')
fanskey = '/' + id + '/' + 'fans'
fansnuminfo = (soup.find_all(attrs={"href": fanskey})[0]).text
fansnum = fansnuminfo[3:-1].encode('utf-8')
userFile.write(id + ' ' + user + ' ' + mcount + ' ' + followsnum + ' ' + fansnum + '\n')
userFile.close()



