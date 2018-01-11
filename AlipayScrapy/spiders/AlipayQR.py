# -*- coding: UTF-8 -*-
"""
Created on 2017年11月1日
@author: Leo
"""

# 系统库
import time
import base64
import requests
from random import choice
from threading import Thread

# 第三方库
import scrapy
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# 项目内部库
from AlipayScrapy.utils.time_util import TimeUtil


ua_list = [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/48.0.2564.82 "
        "Chrome/48.0.2564.82 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 "
        "Safari/537.36"
]


# 支付宝爬虫二维码入口
class AlipayQRCodeSpider(scrapy.Spider):
    name = "AlipayQR"

    def __init__(self, option=None):
        # 初始化浏览器
        self._browser = None

        # 个人中心和交易记录Url
        self._my_url = 'https://my.alipay.com/portal/i.htm'

        # 登录页面URL(quote_plus的理由是会处理斜杠)
        # self._login_url = 'https://auth.alipay.com/login/index.htm?goto=' + quote_plus(self._my_url)
        self._login_url = 'https://auth.alipay.com/login/index.htm'

        # requests的session对象
        self.session = requests.Session()

        # 将请求头添加到session之中
        self.session.headers = {
            'User-Agent': choice(ua_list),
            'Referer': 'https://consumeprod.alipay.com/record/advanced.htm',
            'Host': 'consumeprod.alipay.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive'
        }

        # cookie存储
        self.cookie = {}

        # 交易类别选项(空则默认为1)
        if option is None:
            self.transfer_option = "1"
        else:
            self.transfer_option = str(option)

        # 账单日期筛选
        self.end_date, self.begin_date = TimeUtil.get_front_or_after_month(month=-3)

        super().__init__()

    # 初始化Chrome
    def _load_chrome(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.resourceTimeout"] = 15
        dcap["phantomjs.page.settings.loadImages"] = False
        dcap["phantomjs.page.settings.userAgent"] = choice(ua_list)
        # self._browser = webdriver.Chrome(executable_path="C:\\Python34\\Scripts\\chromedriver.exe")
        self._browser = webdriver.Chrome(executable_path="./AlipayScrapy/conf/chromedriver2-35.exe")

    # 启动
    def start_requests(self):
        # 浏览器初始化配置
        self._load_chrome()
        self._browser.get(self._login_url)
        self._browser.implicitly_wait(3)

        # 点击扫码登录的选项卡
        self._browser.find_element_by_xpath('//*[@id="J-loginMethod-tabs"]/li[1]').click()

        # 保存整体页面截图
        screenshot_base64 = self._browser.get_screenshot_as_base64()
        # print(screenshot_base64)

        # 定位元素
        qr_code_tag = self._browser.find_element_by_id('J-qrcode-img')

        # 获取具体位置
        left = qr_code_tag.location['x']
        top = qr_code_tag.location['y']
        right = qr_code_tag.location['x'] + qr_code_tag.size['width']
        bottom = qr_code_tag.location['y'] + qr_code_tag.size['height']

        # base64还原
        imgdata = base64.b64decode(screenshot_base64)
        file = open('qr_code.jpg', 'wb')
        file.write(imgdata)
        file.close()

        # 裁剪图片
        im = Image.open('qr_code.jpg')
        im = im.crop((left, top, right, bottom))

        # 打开图片
        def open_image(image: Image):
            image.show()

        # 开启一个子线程
        # t1 = Thread(target=open_image, args=(im, ))

        # 关闭之后开始获取数据
        while self._login_url == self._browser.current_url:
            # t1.start()
            if self._login_url != self._browser.current_url:
                # Image.Image.close(im)
                break

        print(self._browser.current_url)
        self._browser.maximize_window()
        time.sleep(10)
        self._browser.close()

    def parse(self, response):
        pass
