# -*- coding: UTF-8 -*-
"""
Created on 2018年3月14日
@author: Leo
"""
# 系统库
import time
import random

# PyMouse
# from pymouse import PyMouse


# 减慢输入速度
def slow_input(ele, word: str):
    for i in word:
        # 输出一个字符
        ele.send_keys(i)
        # 随机睡眠0到1秒
        time.sleep(random.uniform(0, 0.5))


# PyMouse移动
# def mouse_mov_and_click(pos_x: int, pos_y: int):
#     """
#     鼠标移动点击
#     :param pos_x:
#     :param pos_y:
#     :return:
#     """
#     m = PyMouse()
#     m.move(pos_x, pos_y)
#     time.sleep(random.uniform(0.4, 0.7))
#     m.click(pos_x, pos_y)
