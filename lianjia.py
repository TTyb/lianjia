#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import requests
import pandas as pd
from GetDetail import *
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0',
           'Referer': 'm.lianjia.com',
           'Host': 'm.lianjia.com',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
           'Connection': 'keep-alive'
           }

session = requests.session()
url_ori = "https://m.lianjia.com"
print("第一次访问：获取set-cookie", "：", url_ori)
session.get(url_ori, headers=headers)
html_set_cookie = requests.utils.dict_from_cookiejar(session.cookies)


# 解析网页
def getHtml(url, _cookie=None):
    html_bytes = session.get(url, headers=headers, cookies=_cookie)
    html_set_cookie = requests.utils.dict_from_cookiejar(session.cookies)
    return html_set_cookie, html_bytes.content.decode("utf-8", "ignore")


# 获取城市对应的缩写
def getCity(html):
    cityDict = {}
    soup = BeautifulSoup(html, "html.parser")
    citys = soup.find_all("div", attrs={"class": "city_block"})
    for city in citys:
        list_tmp = city.find_all('a')
        for a in list_tmp:
            cityHref = a.get('href')
            cityName = a.get_text()
            cityDict[cityName] = cityHref

    return cityDict


# 获取引导频道
def getChannel(html):
    channelDict = {}
    soup = BeautifulSoup(html, "html.parser")
    channels = soup.find_all("a", attrs={"class": "inner post_ulog"})
    for channel in channels:
        list_tmp = channel.find_all("div", attrs={"class": "name"})
        channelName = list_tmp[0].get_text()
        channelHref = channel.get('href')
        channelDict[channelName] = channelHref
    return channelDict


# 获取便宜的房子
def getHotHouse(allList, top):
    df = pd.DataFrame(allList)
    # 根据首付降序排列
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('max_colwidth', 1000)
    df["rank"] = df['price_f'].rank(ascending=1, method='dense')
    # 选出排名最低的10个
    df_rank = df[df["rank"] <= top]

    return df_rank


# main函数
def getHtmlMain(city, channel, pages, top):
    url_get_city = url_ori + "/city/"
    print("第二次访问：获取城市编码", "：", url_get_city)
    html_set_cookie, html_city = getHtml(url_get_city)
    cityDict = getCity(html_city)
    url_city = url_ori + cityDict[city]
    print("第三次访问：访问获取导航", "：", url_city)
    html_set_cookie, html_city_content = getHtml(url_city, _cookie=html_set_cookie)
    channelDict = getChannel(html_city_content)
    print(channelDict)
    url_channel = url_ori + channelDict[channel]
    html_set_cookie, html_houses_content = getHtml(url_channel, _cookie=html_set_cookie)
    print("第四次访问：获取房子信息", "：", url_channel)
    allList = []
    get_detail = GetDetail(html_set_cookie, pages, url_channel, session)
    if channel == "二手房":
        allList = get_detail.getDetailErshoufang()
    elif channel == "新房":
        allList = get_detail.getDetailLoupan()
    elif channel == "租房":
        allList = get_detail.getDetailZufang()
    print("获取优质房子")
    resultHouse = getHotHouse(allList, top)
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('max_colwidth', 1000)
    print(resultHouse)


if __name__ == "__main__":
    city = "广州"
    channel = "新房"
    pages = 8
    top = 20
    getHtmlMain(city, channel, pages, top)
