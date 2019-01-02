# -*- coding: utf-8 -*- #
"""
Created on 2018年11月30日
@author: Leo
"""
# Python内置库
import re
# Python第三方库
import http.cookiejar
from lxml import etree
import urllib.error as ue
import urllib.request as ur

# 项目内部库
from AlipayScrapy.utils.bill_page_option import *


class AlipayBillParser(object):

    def __init__(self,
                 data_range: str = "today",
                 status: str = "all",
                 keyword: str = "bizNo",
                 key_value: str = "",
                 date_type: str = "createDate",
                 min_amount: int = 0,
                 max_amount: int = 0,
                 fund_flow: str = "all",
                 trade_modes_list: list = None,
                 trade_type: str = "ALL",
                 category_id: str = "",
                 page_num: int = 1,
                 **kwargs):
        """
        支付宝账单页面请求参数
        :param data_range: 交易时间
        :param status: 交易状态
        :param keyword: 关键词
        :param key_value: 关键词对应的值
        :param date_type: 日期类型
        :param min_amount: 最小金额
        :param max_amount: 最大金额
        :param fund_flow: 资金流量
        :param trade_modes_list: 交易方式
        :param trade_type: 交易分类
        :param category_id: 类别ID(暂时不知道有啥用)
        :param page_num: 页码
        :param kwargs: 其他参数(主要是自定义日期的时候使用)
        """
        self._data_range = data_range
        self._status = status
        self._keyword = keyword
        self._key_value = key_value
        self._date_type = date_type
        self._min_amount = min_amount
        self._max_amount = max_amount
        self._fund_flow = fund_flow
        self._trade_modes_list = trade_modes_list
        self._trade_type = trade_type
        self._category_id = category_id
        self._page_num = page_num
        self._kwargs = kwargs

        # date_range
        if self._data_range not in TRADE_TIME:
            raise ValueError("交易时间有误!")
        if self._data_range == "customDate":
            self._begin_date = self._kwargs.get('beginDate')
            self._begin_time = self._kwargs.get('beginTime')
            self._end_date = self._kwargs.get('endDate')
            self._end_time = self._kwargs.get('endTime')
        # status
        if self._status not in TRADE_STATUS:
            raise ValueError("交易状态有误!")
        # keyword
        if self._keyword not in KEYWORD_LIST:
            raise ValueError("交易关键词有误!")
        # min_amount
        if self._min_amount == 0:
            self._min_amount = ""
        # max_amount
        if self._max_amount == 0:
            self._max_amount = ""
        # fund flow
        if self._fund_flow not in MONEY_FLOW:
            raise ValueError("资金流向有误!")
        # trade_modes_list
        if self._trade_modes_list is None:
            self._trade_modes_list = ""
        if len(self._trade_modes_list) > 0 and self._trade_modes_list is not None:
            trade_mode_str = ""
            for trade_mode in self._trade_modes_list:
                trade_mode_str += "&tradeModes={}".format(trade_mode)
            self._trade_modes_list = trade_mode_str
        # trade_type
        if self._trade_type not in TRADE_TYPE:
            raise ValueError("交易分类有误!")
        # page_num
        if self._page_num < 1:
            raise ValueError("页码有误!")

        # 拼接URL
        self._url = "https://consumeprod.alipay.com/record/advanced.htm" \
                    "?dateRange={dateRange}" \
                    "&status={status}" \
                    "&keyword={keyword}" \
                    "&keyValue={keyValue}" \
                    "&dateType={dateType}" \
                    "&minAmount={minAmount}" \
                    "&maxAmount={maxAmount}" \
                    "&fundFlow={fundFlow}" \
                    "&tradeType={tradeType}" \
                    "&categoryId={categoryId}" \
                    "&pageNum={pageNum}".format(dateRange=self._data_range,
                                                status=self._status,
                                                keyword=self._keyword,
                                                keyValue=self._key_value,
                                                dateType=self._date_type,
                                                minAmount=self._min_amount,
                                                maxAmount=self._max_amount,
                                                fundFlow=self._fund_flow,
                                                tradeType=self._trade_type,
                                                categoryId=self._category_id,
                                                pageNum=self._page_num)

    def crawler(self, cookie_dict: dict):
        """
        爬取
        :param cookie_dict: cookie字典
        """
        # 取cookies
        if cookie_dict is not None:
            cookies = " ".join(["{}={};".format(k, v) for k, v in cookie_dict.items()])
        else:
            cookies = ""
        print(cookies)
        # Header
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            # "Accept-Encoding": "gzip, deflate, br",
            # "Accept-Language": "zh-CN,zh;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 "
                          "Safari/537.36",
            "Cookie": cookies,
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://my.alipay.com/portal/i.htm",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "consumeprod.alipay.com",
            "Upgrade-Insecure-Requests": "1"
        }
        print(headers)
        # Request对象
        request = ur.Request(url=self._url, headers=headers)
        # Urllib + cookiejar
        # 保存cookie
        cookie = http.cookiejar.CookieJar()
        handler = ur.HTTPCookieProcessor(cookie)
        opener = ur.build_opener(handler)
        try:
            response = opener.open(request)
            html = response.read().decode("GBK", 'ignore')
            print(html)
            # lxml selector
            selector = etree.HTML(html)

            # 列表信息
            trs = selector.xpath('//table[@class="ui-record-table table-index-bill"]/tbody/tr')

            for tr in trs:
                time_d = re.compile(r'\s+').sub("", tr.xpath('string(td[@class="time"]/p[@class="time-d"])'))
                time_h = re.compile(r'\s+').sub("", tr.xpath('string(td[@class="time"]/p[contains(@class, "time-h")])'))
                print("交易时间: {} {}".format(time_d, time_h))
                memo = tr.xpath('string(td[@class="memo"])').replace("\t", "").replace("\n", "").replace(" ", "")
                print("备注: {}".format(memo))
                name = tr.xpath('string(td[@class="name"])').replace("\t", "").replace("\n", "").replace(" ", "")
                print("交易名称: {}".format(name))
                code = tr.xpath('string(td[@class="tradeNo ft-gray"])').replace("\t", "").replace("\n", "").replace(" ",
                                                                                                                    "")
                print("商家订单号|交易号: {}".format(code))
                other = tr.xpath('string(td[@class="other"])').replace("\t", "").replace("\n", "").replace(" ", "")
                print("对方: {}".format(other))
                amount = tr.xpath('string(td[@class="amount"])').replace("\t", "").replace("\n", "").replace(" ", "")
                print("金额: {}".format(amount))
                status = tr.xpath('string(td[@class="status"])').replace("\t", "").replace("\n", "").replace(" ", "")
                print("交易状态: {}".format(status))
                print("#" * 100)
        except ue.HTTPError:
            print("Cookie已过期!")
