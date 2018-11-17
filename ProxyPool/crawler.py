# -*- coding: utf-8 -*-
import json
from ProxyPool.utils import get_page
from pyquery import PyQuery as pq
import re
import time


class ProxyMetaClass(type):
    def __new__(cls, name, bases, attrs):   # 自定义类的实例化过程
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaClass):

    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print("成功获取到代理", proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()   # tr:gt(0) jquery中的选择器
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])
            time.sleep(5)

    def crawl_goubanjia(self):
        """
        获取Goubanjia
        :return: 代理
        """
        start_url = 'http://www.goubanjia.com'
        html = get_page(start_url)
        if html:
            doc = pq(html)
            tds = doc('td.ip').items()
            for td in tds:
                td.find('p').remove()
                yield td.text().replace(' ', '').replace('\n', '')

    def crawl_xicidaili(self):
        for i in range(1, 10):
            start_url = 'http://www.xicidaili.com/nn/{}'.format(i)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Host': 'www.xicidaili.com',
                'Referer': 'http://www.xicidaili.com/nn/3',
                'Upgrade-Insecure-Requests': '1',
            }
            html = get_page(start_url, options=headers)
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address + ':' + port
                        yield address_port.replace(' ', '')
            time.sleep(5)

    def crawl_ip3366(self):
        """
        获取ip3366
        :return: 代理
        """
        for page in range(1, 6):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            headers = {
                'Host': 'www.ip3366.net',
                'Upgrade-Insecure-Requests': '1',
            }
            time.sleep(5)
            html = get_page(start_url, headers)
            if html:
                ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>', re.S)
                #  \s * 匹配空格，起到换行作用
                ip_addresses = ip_address.findall(html)
                for address, port in ip_addresses:
                    result = address + ":" + port
                    yield result.replace(" ", "")

    def crawl_kuaidaili(self):
        for i in range(1, 4):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            time.sleep(5)
            html = get_page(start_url)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>')
                re_ip_address = ip_address.findall(html)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html)
                for address, port in zip(re_ip_address, re_port):
                    address_port = address + ':' + port
                    yield address_port.replace(' ', '')

    def crawl_iphai(self):
        start_url = 'http://www.iphai.com/'
        html = get_page(start_url)
        if html:
            find_tr = re.compile('<tr>(.*?)</tr>', re.S)
            trs = find_tr.findall(html)
            for s in range(1, len(trs)):
                find_ip = re.compile('<td>\s+(\d+\.\d+\.\d+\.\d+)\s+</td>', re.S)
                re_ip_address = find_ip.findall(trs[s])
                find_port = re.compile('<td>\s+(\d+)\s+</td>', re.S)
                re_port = find_port.findall(trs[s])
                for address, port in zip(re_ip_address, re_port):
                    address_port = address + ':' + port
                    yield address_port.replace(' ', '')

    def crawl_89ip(self):
        for i in range(1, 8):
            start_url = 'http://www.89ip.cn/index_{}.html'.format(i)
            html = get_page(start_url)
            if html:
                find_address_ports = re.compile('(\d+\.\d+\.\d+\.\d+).*?</td>.*?<td>.*?(\d+).*?</td>', re.S)
                address_ports = find_address_ports.findall(html)
                for address, port in address_ports:
                    result = address + ":" + port
                    yield result
            time.sleep(5)
