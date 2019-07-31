from selenium import webdriver
from selenium.webdriver  import ActionChains
import time


def get_track(distance):
    track = []
    current = 0
    mid = distance * 3 / 4
    t = 2
    v = 0
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track
if __name__ == '__main__':
    flag = 0
    distance = 246
    offset = 5
    times = 0
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("User-Agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36")
    driver = webdriver.Chrome("/home/yhl/下载/chromedriver",chrome_options=chrome_options)
    driver.get("https://www.qichacha.com/index_verify?type=companysearch&back=/search?key=%E5%95%8A%E5%95%8A%E5%95%8A")
    button = driver.find_element_by_id("nc_1_n1z")
    # action = ActionChains(driver)
    # action.click_and_hold(button).perform()
    # action.reset_actions()
    # #
    # action.move_by_offset(260, 0).perform()


    while True:
        action = ActionChains(driver)
        action.click_and_hold(button).perform()
        action.reset_actions()	# 清除之前的action

        track = get_track(distance)
        for i in track:
            action.move_by_offset(xoffset=i, yoffset=0).perform()
            action.reset_actions()

        time.sleep(0.5)
        action.release().perform()
        time.sleep(5)
