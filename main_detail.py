import sys
import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
import threading
import requests
from scrapy import Selector
import urllib3
import redis
import time
import random
import re

from qichacha_zhejiang.settings import redis_config,user_agent,mysql_config,proxy_servers
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Process(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        # self.break_status = "iscookie"
        #初始化redis连接
        pool = redis.ConnectionPool(host=redis_config['host'], port=redis_config['port'],
                                    password=redis_config['password'])
        self.r = redis.Redis(connection_pool=pool)
        self.sleep_time = [1.1, 1.3, 1.5, 1, 2, 2.1, 2.3, 2.5, 3.6]
        self.enterprise_id_name = ""




    def run(self):
        while True:

            self.r.set(redis_config['ischangedip'], "change_ip")

            while True:
                try:
                    time.sleep(random.choice(self.sleep_time))
                    headers = {
                        "User-Agent": random.choice(user_agent),
                    }

                    # #获得最新的proxy_ip
                    # proxy_ip = bytes.decode(self.r.mget(redis_config['proxy_pools'])[0])  # 取第一个即可
                    # proxies = {'http': 'http://'+proxy_ip+':8878',
                    #            # 'https': self.proxy
                    #            }



                    # 获得发送信号后更新后的信息
                    ischanged_ip = bytes.decode(self.r.get(redis_config["ischangedip"]))
                    if ischanged_ip == "change_ip":
                        break


                    proxies = {
                        'http': 'http://127.0.0.1:8123',
                        'https': 'https://127.0.0.1:8123',
                    }



                    enterprise_id_name = bytes.decode(self.r.rpop(redis_config["etp_id"]))
                    self.enterprise_id_name = enterprise_id_name

                    enterprise_id = enterprise_id_name.split("##")[0]
                    enterprise_name = enterprise_id_name.split("##")[1]

                    print("1111------", enterprise_name)
                    response = requests.get(
                        'https://www.qichacha.com/firm_{}'.format(enterprise_id),
                        proxies=proxies, verify=False,
                        headers=headers)

                    print("333333333333333333")
                    print(response.text)
                    print(response.status_code)

                    content = response.text
                    if response.status_code != 200:
                        # 再放回去
                        self.r.lpush(redis_config["etp_id"], enterprise_id_name)
                        break

                    if "index_verify" in content or "公司不存在" in content:
                        #再放回去
                        self.r.lpush(redis_config["etp_id"],enterprise_id_name)
                        break

                    fields = self.parse_detail(content)



                    fields = "####".join(fields)

                    print("解析到-------" + fields)
                    print("22222------" + enterprise_name)


                    fields = enterprise_name +"#@@#"+fields

                    self.r.lpush(redis_config['fields'], fields)


                except:
                    # 再放回去
                    self.r.lpush(redis_config["etp_id"], self.enterprise_id_name)

                    break

            time.sleep(10)

    def parse_detail(self, content):

        a = Selector(text=content)

        Corporate_name = ''.join(a.css("h1 ::text").extract()).replace("\r", "").replace("\n", "").replace(
            "\r\n", "").replace("\t", "")
        Representative = ''.join(a.css("div.bpen>a>h2 ::text").extract()).replace("\r", "").replace("\n",
                                                                                                    "").replace(
            "\r\n", "").replace("\t", "")
        zczb = ''.join(a.css("td:contains('注册资本')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                   "").replace(
            "\r\n", "").replace("\t", "")
        if "币" in zczb:
            zczb = zczb.split("币")[0] + "币"

        sjzb = ''.join(a.css("td:contains('实缴资本')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                   "").replace(
            "\r\n", "").replace("\t", "")
        jyzt = ''.join(a.css("td:contains('经营状态')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                   "").replace(
            "\r\n", "").replace("\t", "")
        clrq = ''.join(a.css("td:contains('成立日期')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                   "").replace(
            "\r\n", "").replace("\t", "")
        tyshxydm = ''.join(a.css("td:contains('统一社会信用代码')+td ::text").extract()).replace("\r", "").replace(
            "\n", "").replace("\r\n", "").replace("\t", "")
        if re.search("\w{18}", tyshxydm):
            tyshxydm = re.search("\w{18}", tyshxydm).group()
        nsrsbh = ''.join(a.css("td:contains('纳税人识别号')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                       "").replace(
            "\r\n", "").replace("\t", "")
        zch = ''.join(a.css("td:contains('注册号')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                 "").replace(
            "\r\n", "").replace("\t", "")
        if re.search("\w+", zch):
            zch = re.search("\w+", zch).group()
        zzjgdm = ''.join(a.css("td:contains('组织机构代码')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                       "").replace(
            "\r\n", "").replace("\t", "")
        if re.search("\w{8}-\w", zzjgdm):
            zzjgdm = re.search("\w{8}-\w", zzjgdm).group()
        qylx = ''.join(a.css("td:contains('企业类型')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                   "").replace(
            "\r\n", "").replace("\t", "")
        if re.search("[\u4e00-\u9fa5]+\([\u4e00-\u9fa5]+\)", qylx):
            qylx = re.search("[\u4e00-\u9fa5]+\([\u4e00-\u9fa5]+\)", qylx).group()
        elif re.search("[\u4e00-\u9fa5]+", qylx):
            qylx = re.search("[\u4e00-\u9fa5]+", qylx).group()
        sshy = ''.join(a.css("td:contains('所属行业')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                   "").replace(
            "\r\n", "").replace("\t", "")
        hzrq = ''.join(a.css("td:contains('核准日期')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                   "").replace(
            "\r\n", "").replace("\t", "")
        djjg = ''.join(a.css("td:contains('登记机关')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                   "").replace(
            "\r\n", "").replace("\t", "")
        ssdq = ''.join(a.css("td:contains('所属地区')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                   "").replace(
            "\r\n", "").replace("\t", "")
        ywm = ''.join(a.css("td:contains('英文名')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                 "").replace(
            "\r\n", "").replace("\t", "")
        cym = ''.join(a.css("td:contains('曾用名')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                 "").replace(
            "\r\n", "").replace("\t", "")
        cbrs = ''.join(a.css("td:contains('参保人数')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                   "").replace(
            "\r\n", "").replace("\t", "")
        rygm = ''.join(a.css("td:contains('人员规模')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                   "").replace(
            "\r\n", "").replace("\t", "")
        yyqx = ''.join(a.css("td:contains('营业期限')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                   "").replace(
            "\r\n", "").replace("\t", "")
        qydz = ''.join(a.css("td:contains('企业地址')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                   "").replace(
            "\r\n", "").replace("\t", "")
        if "查看地图" in qydz:
            qydz = qydz.split("查看地图")[0]
        jyfw = ''.join(a.css("td:contains('经营范围')+td ::text").extract()).replace("\r", "").replace("\n",
                                                                                                   "").replace(
            "\r\n", "").replace("\t", "")


        list_1 = [Corporate_name, Representative, zczb, sjzb, jyzt, clrq, tyshxydm, nsrsbh, zch, zzjgdm,
                  qylx, sshy, hzrq, djjg, ssdq, ywm, cym,
                  cbrs, rygm, yyqx, qydz, jyfw]
        list_1 = [e.strip()for e in list_1]
        return list_1



if __name__ == '__main__':
    my_thread = Process()
    my_thread.start()
    my_thread.join()









# if __name__ == '__main__':
#
#     proxys = proxy_servers
#
#     threads = []
#
#     for proxy in proxys:
#         my_thread = Process(proxy)
#         my_thread.start()
#         threads.append(my_thread)
#     for i in threads:
#         i.join()
