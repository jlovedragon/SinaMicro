#/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import urllib,urllib2
import re

url = 'http://www.kuaidaili.com/proxylist/'
ipList = []

for i in range(1, 11):
    ipUrl = url + str(i)
    ipResponse = requests.get(ipUrl)
    ipResponse.encoding = 'utf-8'
    ipSoup = BeautifulSoup(ipResponse.text, 'lxml')

    ipText = (ipSoup.find_all('td'))
    for j in range(0, 80, 8):
        ip = (re.search(r'(\d[\d|\.]*\d)', str(ipText[j]))).group()
        port = (re.search(r'(\d[\d|\.]*\d)', str(ipText[j+1]))).group()
    #    print ip, ":", port
        ipList.append('http://' + ip + ":" + port)
   # print "------------------"

ipCheckUrl = 'http://1111.ip138.com/ic.asp'
for k in range(0, 100):
    proxy = ipList[k]
    print "-----", proxy
    proxies = {'http' : proxy}
    try:
        respond = requests.get(ipCheckUrl, proxies=proxies)
    except:
        continue
    respond.encoding = 'gb2312'
    print respond.status_code
    print "----------------------------------"
