#!/usr/bin/env python
#  -*- coding:utf-8 -*-
# File http_post.py
import urllib2
import json

def http_get():
    url = 'http://192.168.1.13:9999/test'  # 页面的地址
    response = urllib2.urlopen(url)  # 调用urllib2向服务器发送get请求
    return response.read()  # 获取服务器返回的页面信息

def http_post():
    url = 'http://192.168.1.13:9999/test'
    values = {'user': 'Smith', 'passwd': '123456'}
    jdata = json.dumps(values)  # 对数据进行JSON格式化编码
    req = urllib2.Request(url, jdata)  # 生成页面请求的完整数据
    response = urllib2.urlopen(req)  # 发送页面请求
    return response.read()  # 获取服务器返回的页面信息

ret = http_get()
print("RET %r" % (ret))
resp = http_post()
print resp
