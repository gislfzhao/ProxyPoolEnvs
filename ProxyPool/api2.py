# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
from ProxyPool.store_db import RedisClient

redis = RedisClient()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("""
                    <h2>Welcome to Proxy Pool System</h2>
                    <hr>
                    <h3><a href="/random">Get a Random Proxy</a></h3>
                    <h3><a href="/count">Get the total number of Proxy Pool</a></h3>
                    <h3><a href="/all">Get all Proxies of Proxy Pool</a></h3>
                    """)


class RandomHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(redis.random())


class CountHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(str(redis.count()))


class AllHandler(tornado.web.RequestHandler):
    def get(self):
        proxies = redis.all()
        count = len(proxies)



def make_app():
    return tornado.web.Application([(r"/", MainHandler), (r"/random", RandomHandler),
                                    (r"/count", CountHandler), (r"/all", AllHandler)])


if __name__ == '__main__':
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
