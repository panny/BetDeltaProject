#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings()
urllib3.disable_warnings(InsecureRequestWarning)

sys.path.append("../")
from utils.logger import crawler
from utils.request import Request
from utils.decorators import retry


class HttpClient(object):

    @staticmethod
    @retry(times=3, logger=crawler)
    def get(request=requests.Session(), url='', headers=Request.header(), params={}, proxies={}, timeout=30,
            verify=False):
        """

        :rtype:
        """
        proxies = request.proxies if request.proxies else proxies
        response = request.get(url=url, params=params, headers=headers, proxies=proxies, timeout=timeout,
                               verify=verify)
        if response.content:
            return response
        else:
            raise Exception()

    @staticmethod
    @retry(times=3, logger=crawler)
    def post(request=requests.Session(), url='', headers=Request.header(), params={}, data={}, proxies={}, timeout=30,
             verify=False):
        proxies = request.proxies if request.proxies else proxies
        response = request.post(url=url, params=params, data=data, headers=headers, proxies=proxies,
                                timeout=timeout, verify=verify)
        if response.content:
            return response
        else:
            Exception()
