#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import random
from random import randint
from urllib import request, parse

sys.path.append("../")

android = ['8.0', '8.1']
mobile = ['PAR-AL00 Build/HUAWEIPAR-AL00', 'EML-AL00 Build/HUAWEIEML-AL00', 'BLA-AL00 Build/HUAWEIBLA-AL00']


class FakeChromeUA:
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)'
    ]

    chrome_version = f'Chrome/{randint(66, 70)}.0.{randint(0, 3359)}.{randint(0, 126)}'
    wx_os = f'(Linux; Android {random.choice(android)}; {random.choice(mobile)}; wv)'
    mb_os = f'(Linux; Android {random.choice(android)}.0; zh-CN; {random.choice(mobile)})'

    @classmethod
    def get_ua(cls):
        return ' '.join(['Mozilla/5.0', random.choice(cls.os_type), 'AppleWebKit/537.36',
                         '(KHTML, like Gecko)', cls.chrome_version, 'Safari/537.36'])

    @classmethod
    def get_w_ua(cls):
        return ' '.join(['Mozilla/5.0', cls.wx_os, 'AppleWebKit/537.36',
                         '(KHTML, like Gecko) Version/4.0 ', cls.chrome_version,
                         'MQQBrowser/6.2 TBS/45016 Mobile Safari/537.36',
                         'MMWEBID/4922 MicroMessenger/7.0.8.1540(0x27000834)',
                         'Process/tools NetType/WIFI Language/zh_CN ABI/arm64'])

    @classmethod
    def get_m_ua(cls):
        return ' '.join(['Mozilla/5.0', cls.mb_os, 'AppleWebKit/537.36',
                         '(KHTML, like Gecko)', cls.chrome_version,
                         'Mobile Safari/537.36'])

    @classmethod
    def get_m_(cls):
        return ' '.join(['Dalvik/2.1.0', cls.mb_os])


class Request(object):

    @staticmethod
    def header():
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,en-US;q=0.9',
            'Connection': 'keep-alive',
            'User-Agent': FakeChromeUA.get_ua(),
        }

    @staticmethod
    def we_header():
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/wxpic,image/sharpp,image/apng,image/tpg,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.9',
            'Connection': 'keep-alive',
            'User-Agent': FakeChromeUA.get_w_ua(),
        }

    @staticmethod
    def furl(href: str = '', encoding='utf8'):
        href = request.urlparse(href)
        _data = parse.parse_qs(href.query, encoding=encoding)
        tmp = {}
        for k, v in _data.items():
            tmp[k] = ''.join(v)
        return tmp


if __name__ == '__main__':
    pass
