import requests
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    # "Cookie":"UM_distinctid=16bac2b86571e5-0b7fa7b2f2ec47-18211c0a-100200-16bac2b8658a1a; zg_did=%7B%22did%22%3A%20%2216bac2b87e6147-07b859f23a7f99-18211c0a-100200-16bac2b87e7e0%22%7D; acw_tc=3cdfd94415619616627504721e3a416ba07e0d0f73f9abb7c50b8f4cd9; QCCSESSID=q27uptrsqp96kbgn00jdtpdki7; hasShow=1; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1564289206,1564289426,1564289725,1564292192; CNZZDATA1254842228=795296534-1561960854-https%253A%252F%252Fwww.baidu.com%252F%7C1564306836; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201564309237283%2C%22updated%22%3A%201564309237298%2C%22info%22%3A%201563871858357%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22%22%2C%22cuid%22%3A%20%22fab4e0813cb5109da0023d11c9a015cb%22%7D; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1564309237",
    "Cookie":"Hm_lvt_3456bee468c83cc63fb5147f119f1075=1564354785,1564354803; _uab_collina=156435478645082504957378; hasShow=1; UM_distinctid=16c3acfaec955-03877cf2790458-18330b2e-75300-16c3acfaeca247; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1564354803; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201564354784213%2C%22updated%22%3A%201564354801815%2C%22info%22%3A%201564354784241%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.baidu.com%22%7D; zg_did=%7B%22did%22%3A%20%2216c3acfaba110b-07a534b55533b7-18330b2e-75300-16c3acfaba25c1%22%7D; acw_tc=6548ca9b15643547865235186e6156d4311fb84b68fe7ad79ac32a7fe1; CNZZDATA1254842228=2038870554-1564350048-https%253A%252F%252Fwww.baidu.com%252F%7C1564350048; QCCSESSID=j4ftaslnauqoigrpm639uumb36",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
}
num = 0
import time

while True:
    time.sleep(1)
    proxies = {'http': 'http://127.0.0.1:8123', 'https': 'http://127.0.0.1:8123'}
    r = requests.get(
        'https://www.qichacha.com/search?key=xiaomi',
        #                      'https://www.qichacha.com/firm_2c2a4a5d83f570b42fc9a5b92a0dbe75.html',
        #                      proxies=proxies,verify=False,
        headers=headers)

    print(r.status_code)
    print(r.text)
    num += 1
    if "小查为您找到" not in r.text:
        break
    print(num)
#     print(re.findall("(href=\"/firm_.*?html)",r.text))
