# -*- coding: utf-8 -*- #
"""
Created on 2018年7月3日
@author: Leo
"""
# Python内置库
import os
import sys

# Python第三方库
# 通过调用命令行进行调试
# 调用execute这个函数可调用scrapy脚本
from scrapy.cmdline import execute


def start_spider():
    # 设置工程路径，在cmd 命令更改路径而执行scrapy命令调试
    # 获取main文件的父目录，os.path.abspath(__file__) 为__file__文件目录
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(["scrapy", "crawl", "AlipaySpider",
             "-a", "username={}".format("你的账号"),
             "-a", "password={}".format("你的密码")])
    # execute(["scrapy", "crawl", "AlipayQR"])


if __name__ == '__main__':
    start_spider()