#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用requests请求代理服务器
请求http和https网页均适用
"""
from lxml import etree
import requests

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}

# 提取代理API接口，获取1个代理IP
# api_url = "http://dps.kdlapi.com/api/getdps/?orderid=952494948715340&num=1&pt=1&sep=1"
api_url = "http://dps.kdlapi.com/api/getdps/?orderid=972496677679893&num=1&area=%E6%B5%99%E6%B1%9F&pt=1&f_loc=1&f_et=1&dedup=1&format=json&sep=1"

# # 获取API接口返回的代理IP
# proxy = requests.get(api_url).json()
# print(proxy)
# (proxy_ip, area, sep) = proxy['data']['proxy_list'][0].split(',')
# code = proxy['code']
# order_left_count = proxy['data']['order_left_count']
# dedup_count = proxy['data']['dedup_count']
# #
# # 用户名密码认证(私密代理/独享代理)
# username = "3311516271"
# password = "i9uudc4b"
# proxies = {
#     "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip},
#     "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxy_ip}
# }
# print(proxies)
#
# # 白名单方式（需提前设置白名单）
# # proxies = {
# #     "http": "http://%(proxy)s/" % {"proxy": proxy_ip},
# #     "https": "http://%(proxy)s/" % {"proxy": proxy_ip}
# # }
#
# # 要访问的目标网页
# target_url = "http://super-dev.zhilhu.com/servers"
#
# # 使用代理IP发送请求
# response = requests.get(target_url, proxies=proxies, headers=header)
#
# # 获取页面内容
# if response.status_code == 200:
#     print(response.text)


url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=monline_3_dg&wd=%E4%B8%89%E4%BA%9A&oq=%25E8%258B%25B9%25E6%259E%259C&rsv_pq=9a9a9e89000fcb3a&rsv_t=3599ySA464XWDrUN43vt9CuRa18sOuqeP4uwIRJsby%2FijAodVFxUMBSecIaF6TyFi8u4&rqlang=cn&rsv_dl=tb&rsv_enter=0&rsv_btype=t&inputT=9287&rsv_sug3=34&rsv_sug1=52&rsv_sug7=100&rsv_sug2=0&rsv_sug4=11326"
req = requests.get(url, headers=header, timeout=5)
req.encoding = "utf-8"

html = etree.HTML(req.text)
xpath_items = html.xpath('//div[@id="content_left"]//div[contains(@class,"EC_result")]')
data = list()
for key, item in enumerate(xpath_items):
    datum = dict()
    datum['ad_id'] = "".join(item.xpath('./@id'))
    datum['title'] = "".join(item.xpath('.//h3/div/a/text()|.//h3/div/a/font/text()'))
    datum['domain'] = "".join(
        item.xpath('.//div[contains(@class,"f13")]//span[contains(@class,"ec-showurl-line")]/span/text()'))
    data.append(datum)
print(data)
