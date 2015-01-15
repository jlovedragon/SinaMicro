#/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


url = 'http://1111.ip138.com/ic.asp'

proxies = {'http':'http://61.135.137.31:9000',}

respond = requests.get(url, proxies=proxies)

respond.encoding = 'gb2312'

print respond.status_code
