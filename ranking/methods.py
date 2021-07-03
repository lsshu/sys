from urllib.parse import urlencode

import requests
from django.conf import settings
from django.utils import timezone
from lxml import etree

from ranking.models import RankingRegions, RankingProxies
from ranking.user_agent import rand_computer_user_agent, rand_mobile_user_agent


def get_bd_mobile_ranking(*args, **kwargs):
    """
    获取百度m搜索排名
    """
    try:
        url = "https://m.baidu.com/from=844b/s"
        keywords = kwargs.get("keywords", None)
        headers = kwargs.get("headers", {
            'User-Agent': rand_mobile_user_agent()
        })
        proxies = kwargs.get('proxies', {})
        params = {
            "word": keywords, "sa": "tb", "ts": 0, "t_kt": 0, "ie": "utf-8", "ms": 1, "sss": 111
        }
        url += "?" + urlencode(params)
        response = requests.get(url, headers=headers, proxies=proxies, timeout=kwargs.get("timeout", 5))
        response.encoding = "utf-8"
        html = etree.HTML(response.text)
        xpath_items = html.xpath('//div[@id="results"]//div[contains(@class,"ec_ad_results")]')
        data = list()
        for key, item in enumerate(xpath_items):
            for sub_key, sub_item in enumerate(item.xpath('./div[contains(@class,"ec_resitem")]')):
                datum = dict()
                datum['device'] = "mobile"
                datum['position'] = "top" if "".join(item.xpath('./@posid')) == "1" else "bottom"
                datum['ad_id'] = "".join(sub_item.xpath('./@data-rank'))
                datum['title'] = "".join(sub_item.xpath('.//h3/div/text()|.//h3/div/em/text()'))
                datum['domain'] = "".join(
                    sub_item.xpath(
                        './/div[contains(@class,"c-color-source")]//span[contains(@class,"ec-showurl-line")]/span/text()'))
                data.append(datum)
        return data, "success"
    except:
        return False, "get_mobile_ranking_error"


def get_bd_computer_ranking(*args, **kwargs):
    """
    获取百度pc搜索排名
    """
    try:
        url = "https://www.baidu.com/s"
        keywords = kwargs.get("keywords", None)
        headers = kwargs.get("headers", {
            'User-Agent': rand_computer_user_agent()
        })
        proxies = kwargs.get('proxies', {})
        params = {
            "wd": keywords, "oq": keywords, "ie": "utf-8", "f": 8, "rsv_bp": 0, "tn": "monline_3_dg", "rqlang": "cn",
            "rsv_t": "", "rsv_enter": 0, "rsv_btype": "t", "sa": "tb", "rsv_sug3": 34
        }
        url += "?" + urlencode(params)
        response = requests.get(url, headers=headers, proxies=proxies, timeout=kwargs.get("timeout", 5))
        response.encoding = "utf-8"
        html = etree.HTML(response.text)
        xpath_items = html.xpath('//div[@id="content_left"]//div[contains(@class,"EC_result")]')
        data = list()
        for key, item in enumerate(xpath_items):
            datum = dict()
            datum['device'] = "computer"
            datum['position'] = "left"
            datum['ad_id'] = "".join(item.xpath('./@id'))
            datum['title'] = "".join(item.xpath('.//h3/div/a/text()|.//h3/div/a/font/text()'))
            datum['domain'] = "".join(
                item.xpath('.//div[contains(@class,"f13")]//span[contains(@class,"ec-showurl-line")]/span/text()'))
            data.append(datum)
        return data, "success"
    except:
        return False, "get_computer_ranking_error"


def get_proxies(**kwargs):
    """
    获取代理信息
    """
    area = kwargs.get('area', None)
    proxy = kwargs.get('proxy', settings.PROXY_DEFAULT)
    username = settings.PROXY_USERNAME
    password = settings.PROXY_PASSWORD
    order_id = settings.PROXY_ORDER_ID
    api_url = settings.PROXY_API_URL

    if not area or not username or not password:
        return False, "area_username_password"
    region, t = RankingRegions.objects.get_or_create(name=area)
    try:
        proxies = RankingProxies.objects.filter(expires_time__gt=timezone.now(), proxy=proxy, username=username,
                                                password=password, ranking_region=region).get()
    except RankingProxies.DoesNotExist:
        import requests
        import datetime
        params = {
            "orderid": order_id, "format": "json", "area": area,
            "num": 1, "pt": 1, "f_loc": 1,
            "f_et": 1, "dedup": 1, "sep": 1
        }
        api_url += "?" + urlencode(params)
        proxy_response = requests.get(api_url).json()
        # proxy_response = simulation_proxies_response()
        try:
            (proxy_ip, area, sep) = proxy_response['data']['proxy_list'][0].split(',')
            code = proxy_response['code']
            order_count = proxy_response['data']['order_left_count']
            dedup_count = proxy_response['data']['dedup_count']

            expires_time = timezone.now() + datetime.timedelta(seconds=int(sep))
            proxies = RankingProxies.objects.create(proxy=proxy, username=username, password=password, proxies=proxy_ip,
                                                    ranking_region=region, expires_time=expires_time, code=code,
                                                    sep=sep,
                                                    order_count=order_count, dedup_count=dedup_count, area=area)
        except:
            return False, "proxy_response_error"

    return proxies, {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": proxies.username, "pwd": proxies.password,
                                                        "proxy": proxies.proxies},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": proxies.username, "pwd": proxies.password,
                                                         "proxy": proxies.proxies}
    }


def simulation_proxies_response():
    import random
    """
    模拟 获取 代理
    """
    areas = ['佛山', '南宁', '北海', '杭州', '南昌', '厦门', '温州']
    return {
        "code": 0,
        "data": {
            "order_left_count": 100,
            "dedup_count": 1,
            "proxy_list": [
                "{}.{}.{}.{},{},{}".format(random.randint(1, 255), random.randint(1, 255),
                                           random.randint(1, 255), random.randint(1, 255), random.choice(areas),
                                           random.randint(20, 60))
            ]
        }
    }
