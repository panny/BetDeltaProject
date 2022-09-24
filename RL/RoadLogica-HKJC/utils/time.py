#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import datetime
from enum import Enum

sys.path.append("../")


class TimeUnit(Enum):
    DAY = 0
    HOUR = 1
    MINUTE = 2
    SECOND = 3
    WEEK = 4


DEFAULT_FORMAT = '%Y-%m-%d %H:%M:%S'


class Time(object):

    @staticmethod
    def get_format_time(struct_time=None, t_format=DEFAULT_FORMAT):
        """
        日期格式化
        :param struct_time: 日期
        :param t_format: 日期格式 %Y-%m-%d %H:%M:%S
        :return:
        """
        if struct_time and isinstance(struct_time, datetime.datetime):
            return struct_time.strftime(t_format)
        struct_time = struct_time if struct_time else time.localtime(int(time.time()))
        return time.strftime(t_format, struct_time)

    @staticmethod
    def time_calculate(struct_time=None, t_type=TimeUnit.DAY, num=1):
        """
        日期格式化
        :param struct_time: 日期
        :param t_type: 日期单位
        :param num: 日期差
        :return:
        """
        struct_time = struct_time if struct_time else datetime.datetime.now()
        if t_type == TimeUnit.DAY:
            _time = datetime.timedelta(days=num)
        elif t_type == TimeUnit.HOUR:
            _time = datetime.timedelta(hours=num)
        elif t_type == TimeUnit.MINUTE:
            _time = datetime.timedelta(minutes=num)
        elif t_type == TimeUnit.SECOND:
            _time = datetime.timedelta(seconds=num)
        else:
            _time = datetime.timedelta(days=num)
        return struct_time + _time

    @staticmethod
    def convert_time_format_by_timestamp(timestamps, t_format=DEFAULT_FORMAT):
        """
        时间戳格式化
        :param timestamps: 时间戳
        :param t_format: 日期格式
        :return:
        """
        if not isinstance(timestamps, str):
            timestamps = str(timestamps)
        timestamps = timestamps.split('.')[0]
        if len(timestamps) == 13:
            timestamps = timestamps[:-3]
        if len(timestamps) == 10:
            return Time.get_format_time(time.localtime(int(timestamps)), t_format)
        else:
            return f"日期参数错误：{timestamps}"

    @staticmethod
    def convert_time_format_by_string(time_str='', f_format='', b_format=DEFAULT_FORMAT):
        """
        日期格式转换
        :param time_str: 日期字符串
        :param f_format: 日期格式
        :param b_format: 转化后的格式
        :return:
        """
        conv_time = time.strptime(time_str, f_format)
        return Time.get_format_time(conv_time, b_format)

if __name__ == '__main__':
    print(Time.time_calculate(t_type=TimeUnit.MINUTE, num=-5))
    print(datetime.datetime.now())
