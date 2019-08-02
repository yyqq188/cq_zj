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
import MySQLdb
from qichacha_zhejiang.settings import redis_config,user_agent,mysql_config,proxy_servers
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Process(threading.Thread):

    def __init__(self,proxy):
        threading.Thread.__init__(self)
        # self.break_status = "iscookie"
        self.proxy = proxy
        #初始化redis连接
        pool = redis.ConnectionPool(host=redis_config['host'], port=redis_config['port'],
                                    password=redis_config['password'])
        self.r = redis.Redis(connection_pool=pool)
        # #初始化一个mysql连接
        #
        # self.mysql_db = MySQLdb.connect(host=mysql_config['host'], user=mysql_config['user'], passwd=mysql_config['passwd'],
        #                                 port=mysql_config['port'],
        #                                 db=mysql_config['db'])
        #
        # self.mysql_db.set_character_set('utf8')
        # self.mysql_db.cursor().execute('SET NAMES utf8;')
        # self.mysql_db.cursor().execute('SET CHARACTER SET utf8;')
        # self.mysql_db.cursor().execute('SET character_set_connection=utf8;')





    def run(self):
        while True:
            while True:
                try:
                    time.sleep(1)
                    headers = {
                        "User-Agent": random.choice(user_agent),
                    }
                    proxies = {'http': self.proxy, 'https': self.proxy}
                    enterprise_id_name = bytes.decode(self.r.rpop(redis_config["etp_id"]))

                    enterprise_id = enterprise_id_name.split("##")[0]
                    enterprise_name = enterprise_id_name.split("##")[1]
                    response = requests.get(
                        'https://www.qichacha.com/firm_{}'.format(enterprise_id),
                        proxies=proxies, verify=False,
                        headers=headers)


                    content = response.text

                    if "index_verify" in content or "公司不存在" in content:
                        break
                    fields = self.parse_detail(content)



                    fields = "####".join(fields)
                    fields = enterprise_name +"#@@#"+fields

                    self.r.lpush(redis_config['fields'], fields)
                    #
                    #
                    #
                    # # print(fields)
                    # insert_sql = """insert into {}(enterprise_name,
                    #                 Corporate_name,Representative,zczb,sjzb,jyzt,
                    #                 clrq,tyshxydm,nsrsbh,zch,zzjgdm,
                    #                 qylx,sshy,hzrq,djjg,ssdq,
                    #                 ywm,cym,cbrs,rygm,yyqx,
                    #                 qydz,jyfw) values
                    #                 ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',
                    #                 '{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')
                    #
                    #                                 """.format(mysql_config["table"],enterprise_name,
                    #     fields[0], fields[1], fields[2], fields[3], fields[4], fields[5], fields[6], fields[7],
                    #     fields[8], fields[9],
                    #     fields[10], fields[11], fields[12], fields[13], fields[14], fields[15], fields[16], fields[17],
                    #     fields[18], fields[19],
                    #     fields[20], fields[21]
                    # )
                    #
                    # # 放入mysql
                    # # print(insert_sql)
                    # self.mysql_db.cursor().execute(insert_sql)
                    # self.mysql_db.commit()

                except:

                    break

            time.sleep(20)

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

    proxys = proxy_servers

    threads = []

    for proxy in proxys:
        my_thread = Process(proxy)
        my_thread.start()
        threads.append(my_thread)
    for i in threads:
        i.join()
