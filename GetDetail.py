#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
获取html里面索要抓取的html
返回所有页html里面的信息列表
"""

import GetInfo
import json
import time


class GetDetail(object):
    def __init__(self, html_set_cookie, pages, url_channel, session):
        self.html_set_cookie = html_set_cookie
        self.pages = pages
        self.url_channel = url_channel
        self.session = session

    # 获取二手房详情列表
    def getDetailErshoufang(self):
        allList = []
        for i in range(self.pages):
            page = i + 1
            headerJson = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
                          'Referer': self.url_channel + 'pg' + str(page) + '/',
                          'Host': 'm.lianjia.com',
                          'Accept': 'application/json',
                          'Accept-Encoding': 'gzip, deflate',
                          'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                          'X-Requested-With': 'XMLHttpRequest',
                          'Connection': 'keep-alive'
                          }
            url_detail = self.url_channel + "pg" + str(page) + "/"
            print("模拟请求：获取二手房详情", "：", url_detail)
            html_bytes = self.session.get(url_detail, headers=headerJson, cookies=self.html_set_cookie)
            html_detail = html_bytes.content.decode("utf-8", "ignore")
            detailJson = json.loads(html_detail)
            detailArr = GetInfo.getInfoErshoufang(detailJson["body"])
            allList = allList + detailArr
            time.sleep(2)

        return allList

    # 获取楼盘详情列表
    def getDetailLoupan(self):
        allList = []
        for i in range(self.pages):
            page = i + 1
            headerHtml = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
                          'Referer': self.url_channel + 'pg' + str(page) + '/',
                          'Host': 'm.lianjia.com',
                          'Accept': 'application/json',
                          'Accept-Encoding': 'gzip, deflate',
                          'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                          'X-Requested-With': 'XMLHttpRequest',
                          'Connection': 'keep-alive'
                          }
            url_detail = self.url_channel + "pg" + str(page) + "/"
            print("模拟请求：获取新房详情", "：", url_detail)
            html_bytes = self.session.get(url_detail, headers=headerHtml, cookies=self.html_set_cookie)
            html_detail = html_bytes.content.decode("utf-8", "ignore")
            detailArr = GetInfo.getInfoLoupan(html_detail)
            allList = allList + detailArr
            time.sleep(2)
        return allList

    # 获取租房详情列表
    def getDetailZufang(self):
        allList = []
        for i in range(self.pages):
            page = i + 1
            headerJson = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
                          'Referer': self.url_channel + '/',
                          'Host': 'm.lianjia.com',
                          'Accept': 'application/json',
                          'Accept-Encoding': 'gzip, deflate',
                          'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                          'X-Requested-With': 'XMLHttpRequest',
                          'Connection': 'keep-alive'
                          }
            url_detail = self.url_channel + "pg" + str(page) + "/?ajax=1"
            print("模拟请求：获取租房详情", "：", url_detail)
            html_bytes = self.session.get(url_detail, headers=headerJson, cookies=self.html_set_cookie)
            html_detail = html_bytes.content.decode("utf-8", "ignore")
            detailJson = json.loads(html_detail)
            detailArr = GetInfo.getInfoZufang(detailJson["body"])
            allList = allList + detailArr
            time.sleep(2)

        return allList
