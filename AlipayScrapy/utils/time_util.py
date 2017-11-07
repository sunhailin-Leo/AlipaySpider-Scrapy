# -*- coding: UTF-8 -*-
"""
Created on 2017年10月23日
@author: Leo
"""

# 系统内部库
import math
import time
import datetime

# 第三方库
from dateutil.relativedelta import relativedelta


class TimeUtil:
    def __init__(self):
        # 初始化一些日期,时间和时间模板常量
        self.Monday = "周一"
        self.Tuesday = "周二"
        self.Wednesday = "周三"
        self.Thursday = "周四"
        self.Friday = "周五"
        self.Saturday = "周六"
        self.Sunday = "周日"
        
        self.Morning = "上午"
        self.Afternoon = "下午"
        self.Evening = "晚上"
        self.Midnight = "半夜"
        
        self.morning_start = "060000"
        self.afternoon_start = "120000"
        self.evening_start = "180000"
        self.evening_end = "235959"
        self.midnight_start = "000000"
        
        self.time_hms_layout = "%H%M%S"
        self.time_ymd_layout = "%Y%M%D"

    # 获取周几
    def get_week_day(self, date):
        week_day_dict = {
            0: self.Monday,
            1: self.Tuesday,
            2: self.Wednesday,
            3: self.Thursday,
            4: self.Friday,
            5: self.Saturday,
            6: self.Sunday,
        }
        day = date.weekday()
        return week_day_dict[day]

    # 计算日期时间差
    @staticmethod
    def get_time_gap(time_start, time_end):
        start_time_year = int(time_start.split("-")[0])
        start_time_month = int(time_start.split("-")[1])
        start_time_day = int(time_start.split("-")[2])

        end_time_year = int(time_end.split("-")[0])
        end_time_month = int(time_end.split("-")[1])
        end_time_day = int(time_end.split("-")[2])

        return datetime.datetime(end_time_year,
                                 end_time_month,
                                 end_time_day) - datetime.datetime(start_time_year,
                                                                   start_time_month,
                                                                   start_time_day)

    # 计算最大周数
    @staticmethod
    def get_max_week_num(gap):
        if gap >= 0:
            if gap != 0:
                return math.ceil(float(gap / 7))
            else:
                return 0
        else:
            raise ValueError("No time gap or gap is error!")

    # 时间转换为上午,下午,晚上和半夜
    def _divide_time_quantum(self, time_hms, first_time, second_time):
        try:
            if int(time.strftime(self.time_hms_layout, first_time)) <= \
                    int(time.strftime(self.time_hms_layout, time_hms)) < \
                    int(time.strftime(self.time_hms_layout, second_time)):
                return True
            else:
                return False
        except Exception as err:
            print(err.with_traceback(err))
    
    # 判断时间段
    def get_time_quantum(self, time_hms):
        if self._divide_time_quantum(time_hms=time.strptime(time_hms, self.time_hms_layout),
                                     first_time=time.strptime(self.morning_start, self.time_hms_layout),
                                     second_time=time.strptime(self.afternoon_start, self.time_hms_layout)) is True:
            return self.Morning

        elif self._divide_time_quantum(time_hms=time.strptime(time_hms, self.time_hms_layout),
                                       first_time=time.strptime(self.afternoon_start, self.time_hms_layout),
                                       second_time=time.strptime(self.evening_start, self.time_hms_layout)) is True:
            return self.Afternoon

        elif self._divide_time_quantum(time_hms=time.strptime(time_hms, self.time_hms_layout),
                                       first_time=time.strptime(self.evening_start, self.time_hms_layout),
                                       second_time=time.strptime(self.evening_end, self.time_hms_layout)) is True:
            return self.Evening

        elif self._divide_time_quantum(time_hms=time.strptime(time_hms, self.time_hms_layout),
                                       first_time=time.strptime(self.midnight_start, self.time_hms_layout),
                                       second_time=time.strptime(self.morning_start, self.time_hms_layout)) is True:
            return self.Midnight
        else:
            raise ValueError("Variable time_hms is illegal!")

    # 获取当前年月日的前几个月或者后几个月的时间
    @staticmethod
    def get_front_or_after_month(target_date=None, month=0,
                                 day=None, time_format_layout='%Y.%m.%d', timestamp=False):
        """
        :param target_date: str或者是date类型(格式通用,例),如果target_date为空,则默认日期为当天
        :param month: int类型的月份, int < 0 就是前面的月份, int > 0 就是后面的月份
        :param day: int类型的天数,计算后几天的,默认为空,如果不计算后几个月只计算后几天的,month=0即可
        :param time_format_layout: 日期格式化的模板,默认是%Y.%m.%d,输出是2017.11.01
        :param timestamp: 如果timestamp为True则返回时间戳
        :return: 返回target_date和计算完且格式化后的数据
        """
        # 判断目标日期的逻辑
        if target_date is None:
            _date = datetime.datetime.now()
        else:
            # 判断date的类型
            if isinstance(target_date, str):
                _date = datetime.datetime.strptime(target_date, "%Y-%m-%d")
            elif isinstance(target_date, datetime.datetime):
                _date = target_date
            else:
                raise ValueError("Parameter target_date is illegal!")
        _today = _date
        # 判断day的逻辑
        if day is not None:
            if isinstance(day, int):
                _delta = datetime.timedelta(days=int(day))
                _date = _date + _delta
            else:
                raise ValueError("Parameter day is illegal!")
        # 判断month的类型
        if isinstance(month, int):
            _result_date = _date + relativedelta(months=month)
            if timestamp:
                _result_date_ts = int(time.mktime(_result_date.timetuple())) * 1000
                _today_ts = int(time.mktime(_today.timetuple())) * 1000
                return _today_ts, _result_date_ts
            else:
                return _today.strftime(time_format_layout), _result_date.strftime(time_format_layout)
        else:
            raise ValueError("Month is not int,please confirm your variable`s type.")
