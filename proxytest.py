# -*- coding: utf-8 -*-
import requests
from ProxyPool.setting import USER_AGENTS
from random import choice
PROXY_POOL_URL = 'http://127.0.0.1:5000/random'


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
    except Exception as e:
        print("ERROR", e.args)
        return None


def proxy_test():
    headers = {
        'User-Agent': choice(USER_AGENTS)
    }
    proxy = get_proxy()
    proxies = {}
    if proxy is not None:
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
    try:
        response = requests.get('http://httpbin.org/get',headers=headers, proxies=proxies, timeout=20)
        print(response.text)
    except Exception as e:
        print("ERROR", e.args)


if __name__ == '__main__':
    for i in range(10):
        proxy_test()
