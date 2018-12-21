#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
获取html里面索要抓取的信息
返回某一页html里面的信息列表
"""

from bs4 import BeautifulSoup
from lianjia import url_ori


# 获取二手房的详细信息
def getInfoErshoufang(html):
    detailArr = []

    soup = BeautifulSoup(html, "html.parser")
    detailInfo = soup.find_all("div", attrs={"class": "item_list"})
    detailUrl = soup.find_all("a", attrs={"class": "a_mask"})
    details = zip(detailInfo, detailUrl)
    for info_url in details:
        info = info_url[0]
        detailDict = {}
        # 获取标题
        title_tmp = info.find_all("div", attrs={"class": "item_main"})
        detail_title = title_tmp[0].get_text()
        # 获取房屋大小
        size_tmp = info.find_all("div", attrs={"class": "item_other"})
        detail_size = size_tmp[0].get_text()
        # 获取价格单价
        price_total_tmp = info.find_all("span", attrs={"class": "price_total"})
        detail_price_total = price_total_tmp[0].get_text()
        try:
            unit_price_tmp = info.find_all("span", attrs={"class": "unit_price"})
            detail_unit_price = unit_price_tmp[0].get_text()
        except:
            detail_unit_price = "88888888元/平"
        # 获取标签
        tag_tmp = info.find_all("div", attrs={"class": "tag_box"})
        detail_tag = tag_tmp[0].get_text()
        # 获取详情页
        url_a = info_url[1]

        detailDict["title"] = detail_title
        detailDict["size"] = detail_size
        detailDict["room"] = detail_size.split("/")[0]
        detailDict["room_size"] = detail_size.split("/")[1]
        detailDict["room_toward"] = detail_size.split("/")[2]
        detailDict["room_name"] = detail_size.split("/")[3]
        detailDict["price_total"] = detail_price_total
        detailDict["price_t"] = int(float(detail_price_total.replace("万", "").replace("元/月", "")))
        detailDict["price_f"] = int(float(detail_price_total.replace("万", "").replace("元/月", "")) * 0.3)
        detailDict["unit_price"] = detail_unit_price
        detailDict["u_price"] = int(float(detail_unit_price.replace("元/平", "")))
        detailDict["tag"] = detail_tag
        detailDict["url"] = url_ori + url_a.get("href")
        detailArr.append(detailDict)
    return detailArr


# 获取楼盘的详细信息
def getInfoLoupan(html):
    detailArr = []

    soup = BeautifulSoup(html, "html.parser")
    detailInfo = soup.find_all("div", attrs={"class": "main-info"})
    detailUrl = soup.find_all("a", attrs={"class": "resblock-info"})
    details = zip(detailInfo, detailUrl)
    for info_url in details:
        info = info_url[0]
        detailDict = {}
        # 获取标题
        title_tmp = info.find_all("div", attrs={"class": "resblock-name-line"})
        detail_title = title_tmp[0].get_text()
        # 获取房屋位置
        location_tmp = info.find_all("div", attrs={"class": "resblock-location-line"})
        detail_location = location_tmp[0].get_text()
        # 获取标签
        tag_tmp = info.find_all("div", attrs={"class": "resblock-tags-line"})
        detail_tag = tag_tmp[0].get_text()
        # 获取价格单价
        price_total_tmp = info.find_all("div", attrs={"class": "resblock-price"})
        detail_price_total = price_total_tmp[0].get_text()
        detail_price_total_list = detail_price_total.split()
        if len(detail_price_total_list) == 1:
            detail_price_total_list = detail_price_total_list * 4
        # 获取详情页
        url_a = info_url[1]
        detailDict["title"] = detail_title
        detailDict["location"] = detail_location.strip()
        detailDict["size"] = detail_price_total_list[-1]
        detailDict["unit_price"] = detail_price_total_list[0] + detail_price_total_list[1]
        try:
            detailDict["u_price"] = int(float(detail_price_total_list[0]))
            detailDict["price_total"] = int((int(float(detailDict["size"].split("-")[0])) * detailDict["u_price"]) / 10000)
            detailDict["price_t"] = str((int(float(detailDict["size"].split("-")[0])) * detailDict["u_price"]) / 10000) + "万"
            detailDict["price_f"] = int(detailDict["price_total"] * 0.3)
        except Exception as e:
            print(e)
            detailDict["u_price"] = 88888888
            detailDict["price_total"] = 88888888
            detailDict["price_f"] = 88888888
        detailDict["tag"] = detail_tag
        detailDict["url"] = url_ori + url_a.get("href")
        detailArr.append(detailDict)
    return detailArr


# 获取租房的详细信息
def getInfoZufang(html):
    detailArr = []

    soup = BeautifulSoup(html, "html.parser")
    detailInfo = soup.find_all("div", attrs={"class": "content__item"})
    detailUrl = soup.find_all("a")
    details = zip(detailInfo, detailUrl)
    for info_url in details:
        info = info_url[0]
        detailDict = {}
        # 获取标题
        title_tmp = info.find_all("p", attrs={"class": "content__item__title"})
        detail_title = title_tmp[0].get_text().replace(" ", "")
        # 获取房屋大小
        size_tmp = info.find_all("p", attrs={"class": "content__item__content"})
        detail_size = size_tmp[0].get_text().replace(" ", "")
        # 获取标签
        tag_tmp = info.find_all("p", attrs={"class": "content__item__tag--wrapper"})
        detail_tag = tag_tmp[0].get_text().replace(" ", "") if len(tag_tmp) > 0 else ""
        # 获取月租
        price_tmp = info.find_all("p", attrs={"class": "content__item__bottom"})
        detail_price_total = price_tmp[0].get_text().replace(" ", "")
        # 获取详情页
        url_a = info_url[1]

        detailDict["title"] = detail_title
        detailDict["size"] = detail_size
        detailDict["room"] = ""
        detailDict["room_size"] = ""
        detailDict["room_toward"] = ""
        detailDict["room_name"] = ""
        detailDict["price_total"] = detail_price_total
        detailDict["price_t"] = int(float(detail_price_total.replace("元/月", "").strip().split("-")[0]))
        detailDict["price_f"] = int(detailDict["price_t"] * 0.3)
        detailDict["unit_price"] = ""
        detailDict["u_price"] = 88888888
        detailDict["tag"] = detail_tag
        detailDict["url"] = url_ori + url_a.get("href")
        detailArr.append(detailDict)
    return detailArr
