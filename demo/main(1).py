import json
import time
from selenium import webdriver
from utils.JsonUtil import *
from utils import InterceptCode

"""
获取TB详情页数据
"""
class GetDetail:


    def __init__(self,url):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
            """
        })
        self.url = url
    #登录获取二维码
    def log_in_to_get_a_qr_code(self):
        self.driver.find_element_by_xpath(
            '//*[@id="root"]/div/div[2]/div[2]/div/div[1]/div[2]/div[5]/div[3]').click()
        #获取二维码图片
        InterceptCode.get_code()
        while True:
            login = self.driver.find_elements_by_xpath(
                '//*[@id="login-form"]/div[6]/button')
            if len(login) == 0:
                break
            print('请扫码登录')

        time.sleep(5)
        login_cookie = self.driver.get_cookies()
        print(login_cookie)
        Utilities.preservation_cookies(login_cookie)


    # 抓取详情页图片
    def get_detail_image(self):
        img_url_list = []
        imgs = self.driver.find_elements_by_xpath(
            '//*[@id="root"]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[2]/div/div/img')
        for img in imgs:
            img_url = img.get_attribute("src")
            print(img_url)
            img_url_list.append(img_url)
        print(img_url_list)
        return img_url_list
    #启动网页-登录-刷新
    def launch_the_web_page(self):
        self.driver.get(self.url)
        time.sleep(5)
        # 将之前获取的登录 Cookie 设置到当前浏览器会话中
        while True:
            try:
                for cookie in Utilities.read_cookies():
                    # print(cookie)
                    self.driver.add_cookie(cookie)
                self.driver.refresh()
                break
            except Exception as e:
                print(e, 'cookies异常去重新获取cookies')
                GetDetail.log_in_to_get_a_qr_code(self)
                #上接口之后下面return返回二维码登录图片
        for _ in range(20000 // 1000):  # 假设每次滚动50像素，根据需要调整
            print('滑动')
            time.sleep(1)
            self.driver.execute_script("window.scrollBy(0, 1000);")  # 垂直向下滚动50像素

        time.sleep(10)
        return GetDetail.get_detail_image(self)



# # 创建一个浏览器对象，每个线程都有一个独立的浏览器
url = "https://detail.tmall.com/item.htm?ali_refid=a3_430582_1006:1256900155:N:emtiAWsF8+zhhxaiwzc0Aw==:35c60775ec3e2a0a739b3cf778980a81&ali_trackid=1_35c60775ec3e2a0a739b3cf778980a81&id=707613440127&spm=a21n57.1.item.2"
getDetail = GetDetail(url)
result = getDetail.launch_the_web_page()
print(result)
