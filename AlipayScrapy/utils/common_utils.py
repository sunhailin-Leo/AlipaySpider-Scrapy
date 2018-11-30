# -*- coding: UTF-8 -*-
"""
Created on 2018年3月14日
@author: Leo
"""
# 系统库
import time
import random
from ctypes import windll

# 调用DD库
dd_dll = windll.LoadLibrary('./AlipayScrapy/conf/DDx64.dll')


# 减慢输入速度
def slow_input(ele, word: str):
    """
    减慢输入
    :param ele: 元素
    :param word: 需要输入的字符串
    """
    for i in word:
        # 输出一个字符
        ele.send_keys(i)
        # 随机睡眠0到1秒
        time.sleep(random.uniform(0, 0.5))


def mov_mouse(x: int, y: int):
    """
    移动鼠标
    :param x: x坐标
    :param y: y坐标
    """
    dd_dll.DD_mov(x, y)


def mouse_click():
    """
    鼠标左键点击
    """
    dd_dll.DD_btn(1)
    time.sleep(random.uniform(0.2, 0.5))
    dd_dll.DD_btn(2)


def mouse_mov_and_click(x: int, y: int):
    """
    鼠标移动后左键点击
    :param x: x坐标
    :param y: y坐标
    """
    mov_mouse(x=x, y=y)
    time.sleep(random.uniform(0.9, 1.5))
    mouse_click()


def mouse_wheel(mov_times: int = 10):
    """
    鼠标滚轮向后滚10次
    :param mov_times:
    """
    for _ in range(mov_times):
        dd_dll.DD_whl(2)
        time.sleep(random.uniform(0.6, 1))
