import threading
import requests
from scrapy import Selector


class Process(threading.Thread):
    '''
    记录下上次请求的状态，如果状态是false的话，就去重新获取下proxy
    其实这个状态要分的很细,到底是代理出来问题还是网页有问题,这里就一律认为是代理导致的问题
    '''
    def __init__(self):
        threading.Thread.__init__()
        self.last_status = False
        #初始化redis连接

    def check(self,content):

        if content:
            self.last_status = False
        else:
            self.last_status = True

        return self.last_status

    def get_proxy(self):
        # 从队列中得到
        proxy_data = "从redis中获得proxy数据"
        proxy_ip = proxy_data.split(":")[0]
        proxy_port = proxy_data.split(":")[1]
        return proxy_ip, proxy_port

    def get_data(self,proxy_ip, proxy_port, enterprise_id):
        headers = {
            "User-Agent": ""
        }
        proxies = {"http": "http://{}:{}".format(proxy_ip, proxy_port),
                   "https": "https://{}:{}".format(proxy_ip, proxy_port)

                   }
        r = requests.get("url+enterprise_id", headers=headers, proxies=proxies, verify=False)

        return r.text

    def detail_parse(self):
        pass

    def main(self):
        while True:
            if self.last_status:
                proxy_ip, proxy_port = self.get_proxy()
                if  proxy_ip and proxy_port:
                    while True:
                        enterprise_id = "从redis中获得数据"
                        if enterprise_id:
                            r = self.get_data(proxy_ip, proxy_port, enterprise_id)
                            content = r.text
                            if self.check(content):
                                break
                            result = self.detail_parse(Selector(text=content))










if __name__ == '__main__':


    threads = []

    for i in range(5):
        my_thread = Process()
        my_thread.start()
        threads.append(my_thread)
    for i in threads:
        i.join()
