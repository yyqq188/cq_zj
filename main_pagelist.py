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
import re

from qichacha_zhejiang.settings import redis_config,user_agent,proxy_servers
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Process(threading.Thread):
    def __init__(self,proxy):
        threading.Thread.__init__(self)
        self.break_status = "iscookie"
        self.proxy = proxy
        #初始化redis连接
        pool = redis.ConnectionPool(host=redis_config['host'], port=redis_config['port'])
        self.r = redis.Redis(connection_pool=pool)





    def run(self):

        while True:
            # print("restartttttt")
            if "iscookie" in self.break_status:
                # 获得一个新的cookie  从左边取 不删除
                cookie = self.r.lrange(redis_config['cookies'],0,1)[0]
            else:
                # 获得一个新的cookie  从左边取 不删除
                time.sleep(20)
                cookie = self.r.lrange(redis_config['cookies'],0,1)[0]

            while True:
                try:
                    time.sleep(1)
                    headers = {
                        "Cookie":bytes.decode(cookie),
                        "User-Agent": random.choice(user_agent),
                    }
                    proxies = {'http': self.proxy, 'https': self.proxy}

                    print(bytes.decode(cookie))
                    print(random.choice(user_agent))
                    print(proxies)
                    enterprise_name = self.r.rpop(redis_config['etp_name'])

                    response = requests.get(
                        'https://www.qichacha.com/search?key={}'.format(bytes.decode(enterprise_name)),
                        proxies=proxies, verify=False,
                        headers=headers)
                    # print(bytes.decode(enterprise_name))

                    if response.status_code != 200:
                        self.break_status = "iscookie"
                        break

                    content = response.text
                    print(content)
                    if "小查为您找到" not in content:
                        self.break_status = "isproxy"
                        break


                    enterprise_id = self.parse_listpage(content)
                    self.r.lpush(redis_config["etp_id"],enterprise_id)

                except Exception as e:
                    print(e)
                    self.break_status = "isproxy"
                    break



    def parse_listpage(self,content):
        #取第一个就是
        enterprise_id = re.findall("(href=\"/firm_.*?html)", content)[0]
        #href="/firm_9cce0780ab7644008b73bc2120479d31.html
        enterprise_id = enterprise_id.split("_")[1].split("\.")[0]
        print(enterprise_id)
        return enterprise_id




if __name__ == '__main__':

    proxys = proxy_servers

    threads = []

    for proxy in proxys:
        my_thread = Process(proxy)
        my_thread.start()
        threads.append(my_thread)
    for i in threads:
        i.join()
