# -*- coding: utf-8 -*-
from flask import Flask, g
from ProxyPool.store_db import RedisClient

__all__ = ['app']   # 暴露的接口, 对import * 起作用
app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):     # 用于判断对象是否包含对应的属性, g是用来保存全局表量
        g.redis = RedisClient()
        return g.redis


@app.route('/')
def index():
    return """
    <h2>Welcome to Proxy Pool System</h2>
    <hr>
    <h3><a href="/random">Get a Random Proxy</a></h3>
    <h3><a href="/count">Get the total number of Proxy Pool</a></h3>
    """


@app.route('/random')
def get_random():
    """
    获取随机可用代理
    :return: 代理
    """
    conn = get_conn()
    return conn.random()


@app.route('/count')
def get_counts():
    """
    获取代理总量
    :return: 代理数量
    """
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run()
