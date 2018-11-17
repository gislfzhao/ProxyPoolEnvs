# -*- coding: utf-8 -*-
from random import choice

import redis

MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'


class PoolEmptyError(Exception):
    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('代理池已枯竭！')  # 将对象转化为供解释器读取的形式


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: 地址
        :param port: 端口
        :param password: 密码
        """
        # decode_responses=True:写入的键值对中的value为str类型
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理, 设置分数为初始分数
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, {proxy: score})  # score为分数，根据此来排序

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数的代理
        :return: 随机代理
        """
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE, withscores=False)
        if len(result):  # 如果能获取最高分数
            return choice(result)
        else:
            result = self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError  # raise 是用来抛出异常的

    def decrease(self, proxy):
        """
        代理值减一分，分数小于最小值，代理删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(REDIS_KEY,  -1, proxy)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断代理是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(REDIS_KEY, proxy) is None

    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

    def count(self):
        """
        获取代理数量
        :return: 数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE, withscores=True)

    def delete(self):
        """
        删除所有代理
        :return:
        """
        return self.db.zremrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
