#/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Quantin Hsu'

class WeiboUser:
    'USER INFO'
    def __init__(self, id, username, urank, sex, address, mcount, idolnum, fansnum):
        self.id = id # 用户唯一id
        self.username = username # 姓名
        self.urank = urank # 等级
        self.sex = sex # 性别
        self.address = address # 地址
        self.mcount = mcount # 微博数
        self.idolnum = idolnum # 关注人数
        self.fansnum = fansnum # 粉丝人数