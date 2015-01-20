#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Quantin Hsu'

import requests
from bs4 import BeautifulSoup
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
# postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}

if __name__ == '__main__':
	weiboLogin = WeiboLogin('18601346913', 'testsina')
	cookies = weiboLogin.getCookie()
	weiboUser = WeiboUser(-1)
	weiboUser.getUserInfo('http://weibo.cn/yaochen', cookies)
	print weiboUser.id



