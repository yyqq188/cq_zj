import requests

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
}
num = 0
import time

while True:

    while True:
        try:
            time.sleep(1)
            proxies = {'http': 'http://127.0.0.1:8123', 'https': 'http://127.0.0.1:8123'}
            r = requests.get(
                'https://www.qichacha.com/firm_2c2a4a5d83f570b42fc9a5b92a0dbe75.html',
                proxies=proxies, verify=False,
                headers=headers)

            # r1 = requests.get("http://icanhazip.com", proxies=proxies, verify=False)
            # print(r1.text)
            num += 1

            if "小米之家科技有限公司" not in r.text:
                break
            print(num)
        except:
            break

    time.sleep(20)

