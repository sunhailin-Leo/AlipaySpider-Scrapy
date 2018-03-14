# -*- coding: UTF-8 -*-
"""
Created on 2018年3月14日
@author: Leo
"""
# 系统库
import time
import random


# 减慢输入速度
def slow_input(ele, word):
    for i in word:
        # 输出一个字符
        ele.send_keys(i)
        # 随机睡眠0到1秒
        time.sleep(random.uniform(0, 0.5))