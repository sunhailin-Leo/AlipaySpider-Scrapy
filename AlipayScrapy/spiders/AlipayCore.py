# -*- coding: UTF-8 -*-
"""
Created on 2017年11月1日
@author: Leo
"""

# 系统库
import time
import datetime
import random
import logging
import requests
from random import choice

# 第三方库
import scrapy
from selenium import webdriver
from urllib.parse import quote_plus
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# 项目内部库
from AlipayScrapy.items import AlipayBillItem
from AlipayScrapy.items import AlipayUserItem
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

# 日志基本配置(同时写入到文件和输出到控制台)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger()


# 支付宝爬虫Scrapy版本
class AlipaySpider(scrapy.Spider):
    # Scrapy启动的名字
    name = "AlipaySpider"

    def __init__(self, username, password, option=None, *args, **kwargs):
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
        super(AlipaySpider, self).__init__(*args, **kwargs)

    '''
        工具方法(下方)
    '''
    # 初始化Chorme
    def _load_chrome(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.resourceTimeout"] = 15
        dcap["phantomjs.page.settings.loadImages"] = False
        dcap["phantomjs.page.settings.userAgent"] = choice(ua_list)
        self._browser = webdriver.Chrome(executable_path="C:\\Python34\\Scripts\\chromedriver.exe")

    # 减慢账号密码的输入速度
    @staticmethod
    def _slow_input(ele, word):
        for i in word:
            # 输出一个字符
            ele.send_keys(i)
            # 随机睡眠0到1秒
            time.sleep(random.uniform(0, 0.5))

    # set cookies 到 session
    def _set_cookies(self):
        cookie = self.cookie
        self.session.cookies.update(cookie)
        # 输出cookie
        logger.debug(self.session.cookies)
        return True

    # 该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false
    def _is_element_exist(self):
        try:
            self._browser.find_element_by_link_text('下一页')
            return True
        except Exception as err:
            logger.debug("判断是否存在下一页: " + str(err))
            return False

    # 确认账单类型选项的下拉选项(目前只有购物,线下,还款,缴费)
    def _bill_option_control(self):
        # 购物 SHOPPING
        # 线下 OFFLINENETSHOPPING
        # 还款 CCR
        # 缴费 PUC_CHARGE
        if self.transfer_option == "1":
            self._browser.find_element_by_xpath(
                '//ul[@class="ui-select-content"]/li[@data-value="SHOPPING"]').click()
        elif self.transfer_option == "2":
            self._browser.find_element_by_xpath(
                '//ul[@class="ui-select-content"]/li[@data-value="OFFLINENETSHOPPING"]').click()
        elif self.transfer_option == "3":
            self._browser.find_element_by_xpath(
                '//ul[@class="ui-select-content"]/li[@data-value="CCR"]').click()
        elif self.transfer_option == "4":
            self._browser.find_element_by_xpath(
                '//ul[@class="ui-select-content"]/li[@data-value="PUC_CHARGE"]').click()

    '''
        核心解析方法(下方)
    '''
    # 起步方法
    def start_requests(self):
        # 浏览器初始化配置
        self._load_chrome()
        self._browser.maximize_window()
        self._browser.get(self._login_url)
        self._browser.implicitly_wait(3)

        # 点击密码登录的选项卡
        self._browser.find_element_by_xpath('//*[@id="J-loginMethod-tabs"]/li[2]').click()

        # 用户名输入框
        username = self._browser.find_element_by_id('J-input-user')
        username.clear()
        logger.info('正在输入账号.....')
        self._slow_input(username, self.username)
        time.sleep(random.uniform(0.4, 0.8))

        # 密码输入框
        password = self._browser.find_element_by_xpath('//*[@id="password_container"]/input')
        password.clear()
        logger.info('正在输入密码....')
        self._slow_input(password, self.password)

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
            self._slow_input(secure_code, user_input)

            # 验证码界面下一步按钮
            next_button = self._browser.find_element_by_xpath('//*[@id="J-submit"]/input')
            time.sleep(random.uniform(0.5, 1.2))
            next_button.click()

            # 刷新一下
            self._browser.get(self._browser.current_url)

            # 保存cookies
            self.save_cookies()

            try:
                yield scrapy.Request(self._browser.current_url, callback=self.parse_personal, cookies=self.cookie)
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
            self.save_cookies()

            try:
                yield scrapy.Request(self._browser.current_url, callback=self.parse_personal, cookies=self.cookie)
            except BaseException as err:
                self.logger.error(err)
                self.close(self.name, repr(err))
            else:
                self.logger.warning("--SCRAPY: crawl over correctly")
                self.close(self.name, "crawl over")

    def save_cookies(self):
        # 获取cookies转换成字典
        cookies = self._browser.get_cookies()

        # cookie字典
        cookies_dict = {}
        for cookie in cookies:
            if 'name' in cookie and 'value' in cookie:
                cookies_dict[cookie['name']] = cookie['value']
        self.cookie = cookies_dict

    # 解析个人页面
    def parse_personal(self, response):
        # 日志输出
        logger.info("当前页面: " + self._browser.current_url)

        # 个人页面元素选择器对象
        page_sel = scrapy.Selector(response)

        # 花呗
        user_item = AlipayUserItem()
        user_item['user'] = self.username
        user_item['user_rest_huabei'] = \
            page_sel.xpath('string(//div[@class="amount-des"]/p[1]/span[@class="highlight"]/strong)').extract()[0]
        user_item['user_total_huabei'] = \
            page_sel.xpath('string(//div[@class="amount-des"]/p[2]/strong)').extract()[0]
        user_item['user_yeb_rest'] = \
            page_sel.xpath('string(//p[@class="i-assets-mFund-amount"]/strong)').extract()[0]
        user_item['user_yeb_earn'] = \
            page_sel.xpath('string(//a[@id="J-income-num"])').extract()[0]
        user_item['create_time'] = str(int(time.mktime(datetime.datetime.now().timetuple())) * 1000)
        yield user_item

        # 智能等待 --- 1
        time.sleep(random.uniform(0.2, 0.9))

        # 获取完后跳转到账单页面
        self._browser.find_element_by_xpath('//ul[@class="global-nav"]/li[@class="global-nav-item "]/a').click()

        # 账单页面设置
        # 下拉框a标签点击事件触发
        self._browser.find_element_by_xpath('//div[@id="J-datetime-select"]/a[1]').click()

        # 选择下拉框的选项
        self._browser.find_element_by_xpath('//ul[@class="ui-select-content"]/li[@data-value="threeMonths"]').click()
        '''
        self._browser.find_element_by_xpath('//ul[@class="ui-select-content"]/li[@data-value="customDate"]').click()

        # 起始日期和最终日期的初始化
        begin_date_tag = "beginDate"
        end_date_tag = "endDate"

        # 设置起始日期
        remove_start_time_read_only = "document.getElementById('" + begin_date_tag + "')." \
                                                                                     "removeAttribute('readonly')"
        self._browser.execute_script(remove_start_time_read_only)
        ele_begin = self._browser.find_element_by_id(begin_date_tag)
        ele_begin.clear()
        self._slow_input(ele_begin, self.begin_date)

        # 智能等待 --- 1
        time.sleep(random.uniform(1, 2))

        # 设置结束日期
        remove_end_time_read_only = "document.getElementById('" + end_date_tag + "').removeAttribute('readonly')"
        self._browser.execute_script(remove_end_time_read_only)
        ele_end = self._browser.find_element_by_id(end_date_tag)
        ele_end.clear()
        self._slow_input(ele_end, self.end_date)
        '''

        # 智能等待 --- 2
        time.sleep(random.uniform(0.5, 0.9))

        # 选择交易分类
        self._browser.find_element_by_xpath('//div[@id="J-category-select"]/a[1]').click()

        # 选择交易分类项
        self._bill_option_control()

        # 智能等待 --- 3
        time.sleep(random.uniform(1, 2))

        # 按钮(交易记录点击搜索)
        self._browser.find_element_by_id("J-set-query-form").click()
        logger.info("跳转到自定义时间页面....")
        logger.info(self._browser.current_url)

        # 跳转
        yield scrapy.Request(url=self._browser.current_url,
                             callback=self.parse,
                             cookies=self.cookie)

    # 解析账单页面
    def parse(self, response):
        if "checkSecurity" in self._browser.current_url:
            logger.info("当前页面: " + self._browser.current_url)
            logger.info("需要验证,暂时无解决办法,跳出爬虫")

        else:
            # 判断是否存在下一页的标签
            is_next_page = self._is_element_exist()
            logger.info("是否存在下一页: " + str(is_next_page))

            # 账单页面元素选择器对象
            bill_sel = scrapy.Selector(text=self._browser.page_source)

            # 选取的父标签
            trs = bill_sel.xpath("//tbody//tr")

            try:
                # 开始获取第一页的数据
                for tr in trs:
                    bill_info = AlipayBillItem()

                    # 交易时间(年月日)
                    bill_info['transfer_ymd'] = tr.xpath('string(td[@class="time"]/p[1])').extract()[0].strip()

                    # 交易时间(时分秒)
                    bill_info['transfer_hms'] = tr.xpath('string(td[@class="time"]/p[2])'
                                                         ).extract()[0].strip().replace(":", "") + "00"

                    # memo标签(交易备注)
                    try:
                        bill_info['transfer_memo'] = tr.xpath('string(td[@class="memo"]/'
                                                              'div[@class="fn-hide content-memo"]/'
                                                              'div[@class="fn-clear"]/p[@class="memo-info"])'
                                                              ).extract()[0].strip()
                    except IndexError:
                        logger.debug("Transfer memo exception: transfer memo is empty!")
                        bill_info['transfer_memo'] = ""

                    # 交易名称
                    try:
                        bill_info['transfer_name'] = tr.xpath('string(td[@class="name"]/p/a)').extract()[0].strip()
                    except IndexError:
                        try:
                            bill_info['transfer_name'] = \
                                tr.xpath('string(td[@class="name"]/p/text())').extract()[0].strip()
                        except IndexError:
                            logger.debug("Transfer name exception 2: Transfer name is empty!")
                            bill_info['transfer_name'] = ""

                    # 交易订单号(商户订单号和交易号)
                    code = tr.xpath('string(td[@class="tradeNo ft-gray"]/p)').extract()[0]
                    if "流水号" in code:
                        bill_info['transfer_serial_num'] = code.split(":")[-1]
                        bill_info['transfer_seller_code'] = ""
                        bill_info['transfer_transfer_code'] = ""
                    else:
                        code_list = code.split(" | ")
                        bill_info['transfer_serial_num'] = ""
                        bill_info['transfer_seller_code'] = (str(code_list[0]).split(":"))[-1]
                        bill_info['transfer_transfer_code'] = (str(code_list[-1]).split(":"))[-1]

                    # 对方(转账的标签有不同...奇葩的设计)
                    if bill_info['transfer_memo'] == "":
                        bill_info['transfer_opposite'] = \
                            tr.xpath('string(td[@class="other"]/p[@class="name"]/span)'
                                     ).extract()[0].strip()

                        if bill_info['transfer_opposite'] == "":
                            bill_info['transfer_opposite'] = \
                                tr.xpath('string(td[@class="other"]/p[@class="name"])'
                                         ).extract()[0].strip()
                    else:
                        bill_info['transfer_opposite'] = \
                            tr.xpath('string(td[@class="other"]/p[@class="name"]/span)'
                                     ).extract()[0].strip()

                        if bill_info['transfer_opposite'] == "":
                            bill_info['transfer_opposite'] = \
                                tr.xpath('string(td[@class="other"]/p)'
                                         ).extract()[0].strip()

                    # 输出测试
                    yield bill_info

                # 判断是否存在下一页的标签
                if is_next_page:
                    # 智能等待 --- 3
                    time.sleep(random.uniform(0.3, 0.6))

                    # 抓取完当页的数据后,滚动事件到底部，点击下一页
                    self._browser.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);")

                    # 智能等待 --- 4
                    time.sleep(random.uniform(0.5, 0.9))

                    # 点击下一页
                    next_page_btn = self._browser.find_element_by_link_text('下一页')
                    next_page_btn.click()
                    yield scrapy.Request(url=self._browser.current_url,
                                         callback=self.parse,
                                         cookies=self.cookie,
                                         dont_filter=True)
                else:
                    # 不存在下一页后结束
                    self._browser.close()
                    return
            except Exception as err:
                logger.debug(err.with_traceback(err))
                logger.error('抓取出错,页面数据获取失败')
