# -*- coding: utf-8 -*-
from ProxyPool.getter import Getter
from ProxyPool.tester import Tester
import os

# g = Getter()
# # g.redis.delete()
# g.run()
# # print(g.redis.all())
# print(g.redis.count())

# t = Tester()
# t.run()

# os.chdir(r"C:\Users\GISzhao\Desktop\ProxyPoolEnvs\Scripts")
# os.system('activate')
# os.chdir(r"C:\Users\GISzhao\Desktop\ProxyPoolEnvs\ProxyPool")
# os.system(r'python36  api.py')
from ProxyPool.schedule import Schedule
import requests

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


if __name__ == '__main__':
    s = Schedule()
    s.run()

# while True:
#     print(get_proxy())
