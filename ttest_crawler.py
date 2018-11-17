# -*- coding: utf-8 -*-
from ProxyPool.crawler import Crawler


c = Crawler()
proxies = c.crawl_89ip()
for proxy in proxies:
    print(proxy)
