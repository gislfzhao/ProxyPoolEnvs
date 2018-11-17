# -*- coding: utf-8 -*-
from multiprocessing import Process
from ProxyPool.api import *
from ProxyPool.getter import Getter
from ProxyPool.tester import Tester
import time
import os

TEST_CYCLE = 500
CETTER_CYCLE = 1000
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLE = True


class Schedule:
    def schedule_tester(self, cycle=TEST_CYCLE):
        """
        定时测试代理
        :param cycle:
        :return:
        """
        tester = Tester()
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_ENABLED):
        """
        定时获取代理
        :param cycle:
        :return:
        """
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        """
        开启API
        :return:
        """
        # os.chdir(r"C:\Users\GISzhao\Desktop\ProxyPoolEnvs\Scripts")
        # os.system('activate')
        # os.chdir(r"C:\Users\GISzhao\Desktop\ProxyPoolEnvs\ProxyPool")
        # os.system(r'python36  api.py')
        app.run()

    def run(self):
        print("代理池开始运行")
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester, args=())
            tester_process.start()
        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter, args=())
            getter_process.start()
        if API_ENABLE:
            api_process = Process(target=self.schedule_api, args=())
            api_process.start()

