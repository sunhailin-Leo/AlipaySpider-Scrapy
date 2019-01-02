# -*- coding: UTF-8 -*-
"""
Created on 2017年11月30日
@author: Leo
"""
# 系统库
import datetime
import logging
import requests
from random import choice

# 第三方库
import scrapy
import win_unicode_console
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# 项目内部库
from AlipayScrapy.items import AlipayUserItem
from AlipayScrapy.utils.time_util import TimeUtil
from AlipayScrapy.utils.common_utils import *
from AlipayScrapy.utils.bill_parser import AlipayBillParser

# 解决Win10 console框报错问题
win_unicode_console.enable()

# USERAGENT-LIST
ua_list = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 "
    "Safari/537.36 "
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 "
    "Safari/537.36"
]

# 日志基本配置(同时写入到文件和输出到控制台)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger()


# 支付宝爬虫Scrapy版本
class AlipaySpider(scrapy.Spider):
    # Scrapy启动的名字
    name = "AlipayCore"

    def __init__(self, username, password, option=None, *args):
        # 初始化浏览器
        self._browser = None

        # 初始化用户名和密码
        self.username = username
        self.password = password

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

        # super方法
        super(AlipaySpider, self).__init__(*args)

    '''
        工具方法(下方)
    '''

    # 初始化Chrome
    def _load_chrome(self):
        options = webdriver.ChromeOptions()
        options.add_argument('disable-infobars')
        options.add_argument('--user-agent=%s' % choice(ua_list))
        options.add_experimental_option('prefs', {'download.default_directory': '.\\static\\temp_file\\'})
        self._browser = webdriver.Chrome(executable_path="./AlipayScrapy/conf/chromedriver2-35.exe",
                                         chrome_options=options)

    # set cookies 到 session
    def _set_cookies(self):
        cookie = self.cookie
        self.session.cookies.update(cookie)
        # 输出cookie
        logger.debug(self.session.cookies)
        return True

    def _save_cookies(self):
        # 获取cookies转换成字典
        cookies = self._browser.get_cookies()

        # cookie字典
        cookies_dict = {}
        for cookie in cookies:
            if 'name' in cookie and 'value' in cookie:
                cookies_dict[cookie['name']] = cookie['value']
        self.cookie = cookies_dict

    # 起步方法
    def start_requests(self):
        # 浏览器初始化配置
        self._load_chrome()
        self._browser.maximize_window()
        self._browser.get(self._login_url)

        # 点击密码登录的选项卡
        self._browser.find_element_by_xpath('//*[@id="J-loginMethod-tabs"]/li[2]').click()

        # 用户名输入框
        username = self._browser.find_element_by_id('J-input-user')
        username.clear()
        logger.info('正在输入账号.....')
        slow_input(username, self.username)
        time.sleep(random.uniform(0.4, 0.8))

        # 密码输入框
        password = self._browser.find_element_by_xpath('//*[@id="password_container"]/input')
        password.clear()
        logger.info('正在输入密码....')
        slow_input(password, self.password)

        # 登录按钮
        time.sleep(random.uniform(0.3, 0.5))
        self._browser.find_element_by_id('J-login-btn').click()

        # 输出当前链接
        logger.info("当前页面链接: " + self._browser.current_url)

        # 判断当前页面链接
        if "checkSecurity" in self._browser.current_url:
            logger.info("进入了验证码界面!")
            logger.info("当前页面: " + self._browser.current_url)

            # 手机验证码输入框
            secure_code = self._browser.find_element_by_id("riskackcode")

            # 一次清空输入框
            secure_code.click()
            secure_code.clear()

            logger.info("输入验证码:")
            user_input = input()

            # 防止一些操作失误，二次清空输入框
            secure_code.click()
            secure_code.clear()

            # 开始输入用户提供的验证码
            slow_input(secure_code, user_input)

            # 验证码界面下一步按钮
            next_button = self._browser.find_element_by_xpath('//*[@id="J-submit"]/input')
            time.sleep(random.uniform(0.5, 1.2))
            next_button.click()

            # 刷新一下
            self._browser.get(self._browser.current_url)

            # 保存cookies
            self._save_cookies()

            try:
                yield scrapy.Request(self._browser.current_url, callback=self.parse, cookies=self.cookie)
            except BaseException as err:
                self.logger.error(err)
                self.close(self.name, repr(err))
            else:
                self.logger.warning("--SCRAPY: crawl over correctly")
                self.close(self.name, "crawl over")

        else:
            logger.info("没有进入验证码界面,进入账单页面")
            logger.info("当前页面: " + self._browser.current_url)

            # 保存cookies
            self._save_cookies()

            try:
                yield scrapy.Request(self._browser.current_url, callback=self.parse, cookies=self.cookie)
            except BaseException as err:
                self.logger.error(err)
                self.close(self.name, repr(err))
            else:
                self.logger.warning("--SCRAPY: crawl over correctly")
            self.close(self.name, "crawl over")

    # 解析个人页面
    def parse(self, response):
        # 日志输出
        logger.info("当前页面: " + self._browser.current_url)

        # 点击账户余额、余额宝、花呗的显示金额按钮(JS注入的方式)
        try:
            show_account_button = self._browser.find_element_by_xpath('//*[@id="showAccountAmount"]/a[1]')
            show_account_button.click()
            time.sleep(random.uniform(0.3, 0.9))
        except NoSuchElementException:
            pass
        try:
            show_yuerbao_button = self._browser.find_element_by_xpath('//*[@id="showYuebaoAmount"]/a[1]')
            show_yuerbao_button.click()
            time.sleep(random.uniform(0.3, 0.9))
        except NoSuchElementException:
            pass
        try:
            show_huabei_button = self._browser.find_element_by_xpath('//*[@id="showHuabeiAmount"]/a[1]')
            show_huabei_button.click()
        except NoSuchElementException:
            pass

        # 等待
        time.sleep(2)

        # 个人页面元素选择器对象
        page_sel = scrapy.Selector(text=self._browser.page_source)

        # 构造数据
        user_item = AlipayUserItem()
        user_item['user'] = self.username
        user_item['user_rest_huabei'] = \
            page_sel.xpath('string(//*[@id="available-amount-container"]/span)').extract_first()
        user_item['user_total_huabei'] = \
            page_sel.xpath('string(//*[@id="credit-amount-container"]/span)').extract_first()
        user_item['user_yeb_earn'] = \
            page_sel.xpath('string(//a[@id="J-income-num"])').extract_first()
        user_item['user_yeb_rest'] = \
            page_sel.xpath('string(//*[@id="J-assets-mfund-amount"]/span)').extract_first()
        user_item['create_time'] = str(int(time.mktime(datetime.datetime.now().timetuple())) * 1000)
        yield user_item

        # 获取cookie
        print(self.cookie)

        # 点击交易记录选项卡
        # self._browser.find_element_by_xpath('//ul[@class="global-nav"]/li[@class="global-nav-item "]/a').click()
        # mouse_mov_and_click(x=1180, y=160)

        self._browser.get('https://consumeprod.alipay.com/record/advanced.htm')

        # 爬取账单
        alipay_bill_spider = AlipayBillParser()
        alipay_bill_spider.crawler(cookie_dict=self.cookie)
