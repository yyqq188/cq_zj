import threading
import requests
from scrapy import Selector
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Process(threading.Thread):
    '''
    记录下上次请求的状态，如果状态是false的话，就去重新获取下proxy
    其实这个状态要分的很细,到底是代理出来问题还是网页有问题,这里就一律认为是代理导致的问题
    '''
    def __init__(self,proxy):
        threading.Thread.__init__()
        self.last_status = False
        self.proxy = proxy
        #初始化redis连接


    def check_detail(self,content):
        if content:
            self.last_status = False
        else:
            self.last_status = True

        return self.last_status

    def check_listpage(self,content):

        if content:
            self.last_status = False
        else:
            self.last_status = True

        return self.last_status



    def get_data_listpage(self,proxy, enterprise_name):
        headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        proxies = {"http": "http://{}".format(proxy),
                   "https": "https://{}".format(proxy)

                   }
        r = requests.get("url+enterprise_name", headers=headers, proxies=proxies, verify=False)

        return r.text


    def get_data_detail(self,proxy, enterprise_id):
        headers = {
            "User-Agent":
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }
        proxies = {"http": "http://{}".format(proxy),
                   "https": "https://{}".format(proxy)

                   }
        r = requests.get("url+enterprise_id", headers=headers, proxies=proxies, verify=False)

        return r.text



    def parse_detail(self):
        pass


    def parse_listpage(self):
        pass

    def run(self):
        while True:
            if self.last_status:

                #执行更新proxy的操作
                #pass





                while True:

                    enterprise_name = "从redis中读到企业名称"
                    if enterprise_name:
                        r = self.get_data_listpage(self.proxy,enterprise_name)
                        content = r
                        if self.check_listpage(content):
                            #redis.lpush(enterprise_name)
                            break

                        enterprise_id = self.parse_listpage(Selector(text=content))


                        r = self.get_data_detail(self.proxy, enterprise_id)
                        content = r
                        if self.check_detail(content):
                            #redis.lpush(enterprise_name)
                            break
                        result = self.parse_detail(Selector(text=content))














if __name__ == '__main__':

    proxys = ["http://127.0.0.1:8123","http://127.0.0.1:8123"
              "http://127.0.0.1:8123","http://127.0.0.1:8123","http://127.0.0.1:8123"]
    threads = []

    # for i in proxys:
    #     my_thread = Process(i)
    #     my_thread.start()
    #     threads.append(my_thread)
    # for i in threads:
    #     i.join()
    for i in range(5):
        my_thread = Process(i)
        my_thread.start()
        threads.append(my_thread)
    for i in threads:
        i.join()