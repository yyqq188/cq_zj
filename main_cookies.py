import sys
import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
import redis
from qichacha_zhejiang.settings import redis_config
from selenium import webdriver
import time

class Cookie_Process(object):
    def __init__(self):
        pool = redis.ConnectionPool(host=redis_config['host'],port=redis_config['port'])
        self.r = redis.Redis(connection_pool=pool)

        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--no-sandbox")

        # chrome_options.add_argument("--proxy-server=http://39.106.163.125:8124")
        # chrome_options.add_argument("--proxy-type=socks5")

        #这里是本地和docker环境不同的地方
        # self.client = webdriver.Chrome(executable_path="/home/yhl/下载/chromedriver", chrome_options=chrome_options)
        self.client = webdriver.Chrome(chrome_options=chrome_options)
        super(Cookie_Process, self).__init__()

    def close_brower(self):
        self.client.quit()

    def get_cookie(self):
        self.client.get("https://www.baidu.com/s?wd=企查查")

        self.client.find_elements_by_xpath("//input[@value='百度一下']")[0].click()
        time.sleep(1.5)

        self.client.find_element_by_xpath("//div[@class='result c-container 'and @id='1']//a[1]").click()
        time.sleep(1.5)

        print("change to new window")
        all_windows = self.client.window_handles
        self.client.switch_to_window(all_windows[1])

        print("reload")


        self.client.refresh()
        time.sleep(1.5)
        kvs = []
        for e in self.client.get_cookies():
            kv = e['name']+"="+e['value']
            print(kv)
            kvs.append(kv)
        current_cookie = "; ".join(kvs)
        print(current_cookie)
        #把生成的cookie推送到reids中
        self.r.lpush(redis_config['cookies'],current_cookie)
        
        import hashlib
        hexdigest_str = hashlib.sha1(current_cookie.encode()).hexdigest()
        print("----- ",hexdigest_str)
        print("close the brower")
        self.close_brower()

if __name__ == '__main__':

    #这里是本地和docker环境不同的地方
    # while True:
    #     time.sleep(1)
    cookie_process = Cookie_Process()
    cookie_process.get_cookie()
    sys.exit(0)