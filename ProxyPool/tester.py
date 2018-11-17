# -*- coding: utf-8 -*-
import asyncio
import aiohttp
import time
import sys
from aiohttp import ClientError
from aiohttp import ClientProxyConnectionError
from ProxyPool.store_db import RedisClient

VALID_STATUS_CODE = [200]
TEST_URL = 'http://www.baidu.com'
BATH_TEST_SIZE = 50


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        测试单个代理
        :param proxy: 单个代理
        :return:
        """
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            if isinstance(proxy, bytes):
                proxy = proxy.decode('utf-8')
            try:
                real_proxy = 'http://' + proxy
                print('正在测试', proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=20, allow_redirects=False) as response:
                    if response.status in VALID_STATUS_CODE:
                        self.redis.max(proxy)
                        print("代理可用", proxy)
                    else:
                        self.redis.decrease(proxy)
                        print("代理请求失败", proxy)
            except (ClientError, ClientProxyConnectionError, asyncio.TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print("代理请求失败", proxy)

    def run(self):
        """
        测试主函数
        :return:
        """
        print('测试器开始运行')
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            count = self.redis.count()
            print('当前剩余', count, '个代理')
            # 批量测试
            for i in range(0, len(proxies), BATH_TEST_SIZE):
                start = i
                stop = min(i + BATH_TEST_SIZE, count)
                print('正在测试第', start + 1, '-', stop, '个代理')
                test_proxies = proxies[start:stop]
                tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print("测试器异常", e.args)

