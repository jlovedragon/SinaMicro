#/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Quantin Hsu'

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class WeiboLogin:
    " get cookie "
    def __init__(self, username, password, enableProxy = False):
        print "Initializing WeiboLogin..."
        self.username = username
        self.password = password
        self.enableProxy = enableProxy

        self.loginUrl = 'http://login.weibo.cn/login/'
        self.postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}

    def login(self):
        self.EnableProxies(self.enableProxy)

    def enableProxies(self):
        pass

    def getCookie(self):
        driver = webdriver.Chrome()
        driver.get("http://login.weibo.cn/login/")
        username = driver.find_element_by_css_selector("input[name=mobile]")
        username.send_keys(self.username)
        password = driver.find_element_by_css_selector('input[name^=password]')
        password.send_keys(self.password)
        rem = driver.find_element_by_css_selector('input[name=remember]')
        rem.click()
        submit = driver.find_element_by_css_selector('input[name=submit]')
        submit.click()
        cookieSet = driver.get_cookies()
        cookies = {}
        for iCookie in cookieSet:
            name = iCookie['name']
            value = iCookie['value']
            cookies[name] = value

            # if name == 'gsid_CTandWM':
                # cookie = dict(name=value)
        driver.close()
        # print cookies
        return cookies


if __name__ == '__main__':
    weiboLogin = WeiboLogin('18601346913', 'testsina')
    cookie = weiboLogin.getCookie()
    print cookie