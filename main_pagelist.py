import sys
import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

import threading
import requests
import urllib3
import redis
import time
import random
from scrapy import Selector

from qichacha_zhejiang.settings import redis_config,user_agent
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Process(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.break_status = "iscookie"
        #初始化redis连接
        pool = redis.ConnectionPool(host=redis_config['host'], port=redis_config['port'],
                                    password=redis_config['password'])
        self.r = redis.Redis(connection_pool=pool)
        self.sleep_time = [1.1, 1.3, 1.5, 1, 2, 2.1, 2.3, 2.5, 3.6]

        self.enterprise_name = ""


    def run(self):

        while True:
            if "iscookie" in self.break_status:
                # 获得一个新的cookie  从左边取 不删除
                cookie = self.r.lrange(redis_config['cookies'],0,1)[0]
                self.r.set(redis_config['ischangedip'], "change_ip")

            else:
                # 获得一个新的cookie  从左边取 不删除
                cookie = self.r.lrange(redis_config['cookies'], 0, 1)[0]

                # time.sleep(20)
                #就不是等待时间了，而是发送重新
                self.r.set(redis_config['ischangedip'],"change_ip")


            while True:
                try:
                    time.sleep(random.choice(self.sleep_time))
                    headers = {
                        "Cookie":bytes.decode(cookie),
                        # "Cookie":"domain=.globalsign.com;",
                        "User-Agent": random.choice(user_agent),
                    }
                    # # 获得最新的proxy_ip
                    # proxy_ip = bytes.decode(self.r.mget(redis_config['proxy_pools'])[0])  # 取第一个即可
                    # proxies = {'http': 'http://'+proxy_ip+':8878',
                    #            # 'https': self.proxy
                    #            }


                    #获得发送信号后更新后的信息
                    ischanged_ip = bytes.decode(self.r.get(redis_config["ischangedip"]))
                    if ischanged_ip == "change_ip":

                        self.break_status = "isproxy"
                        break





                    proxies = {
                        'http': 'http://127.0.0.1:8123',
                        'https': 'https://127.0.0.1:8123',
                    }



                    enterprise_name = self.r.rpop(redis_config['etp_name'])
                    enterprise_name = bytes.decode(enterprise_name)
                    self.enterprise_name = enterprise_name
                    print("1111------", enterprise_name)
                    response = requests.get(
                        'https://www.qichacha.com/search?key={}'.format(enterprise_name),
                        proxies=proxies, verify=False,
                        headers=headers,timeout=5)
                    print("333333333333333333")
                    print(response.text)
                    print(response.status_code)
                    if response.status_code != 200:
                        #再放回去
                        self.r.lpush(redis_config['etp_name'],enterprise_name)
                        self.break_status = "iscookie"
                        break

                    content = response.text

                    if "小查为您找到" not in content:
                        # 再放回去
                        self.r.lpush(redis_config['etp_name'], enterprise_name)
                        self.break_status = "isproxy"
                        break



                    enterprise_id = self.parse_listpage(content)
                    print("解析到-------"+enterprise_id)
                    print("22222------" + enterprise_name)
                    #加上enterprise_id 和 enterprise_name
                    if enterprise_id:
                        self.r.lpush(redis_config["etp_id"],enterprise_id+"##"+enterprise_name)

                except Exception as e:
                    # # 再放回去   #这里要给个全局变量
                    self.r.lpush(redis_config['etp_name'], self.enterprise_name)
                    self.break_status = "isproxy"
                    break



    def parse_listpage(self,content):
        print(content)
        content = Selector(text=content)
        content = content.css("#search-result >tr:nth-child(1)>td:nth-child(3)>a ::attr(href)").extract()
        if len(content) == 1:
            enterprise_id = content[0].split("_")[1]

        else:
            enterprise_id = ''

        return enterprise_id

if __name__ == '__main__':
    my_thread = Process()
    my_thread.start()
    my_thread.join()

    # proxys = proxy_servers
    #
    # threads = []
    #
    # for proxy in proxys:
    #     my_thread = Process(proxy)
    #     my_thread.start()
    #     threads.append(my_thread)
    # for i in threads:
    #     i.join()
