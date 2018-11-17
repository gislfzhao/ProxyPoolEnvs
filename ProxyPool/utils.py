# -*- coding: utf-8 -*-
import requests
from random import choice
from ProxyPool.setting import USER_AGENTS
from requests.exceptions import ConnectionError

PROXY_POOL_URL = 'http://127.0.0.1:5000/random'


def get_user_agent():
    """
    获取随机的浏览器
    :return: 浏览器字符串
    """
    return choice(USER_AGENTS)


def get_proxy():
    """
    获取随机可用的代理
    :return: 代理
    """
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
    except Exception as e:
        print("ERROR", e.args)
        return None


base_headers = {
    'User-Agent': get_user_agent(),
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
}


def get_page(url, options={}):
    """
    抓取代理
    :param url: 链接
    :param options: 可选参数
    :return: 响应文本
    """
    count = 0
    while count < 5:
        headers = dict(base_headers, **options)
        print("正在抓取", url)
        proxy = get_proxy()
        proxies = {}
        if proxy is not None:
            proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=30)
            if response.status_code == 200:
                print('抓取成功', url, response.status_code)
                return response.text
            else:
                print('抓取失败', url, response.status_code)
        except ConnectionError:
            print('抓取失败', url)
        except BaseException as e:
            print('运行出错', e)
        count += 1
    return None
