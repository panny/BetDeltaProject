#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import json
from functools import wraps, partial
from django.http import JsonResponse

sys.path.append("../")
from utils.logger import other


def retry(times=3, delay=0, exceptions=Exception, logger=other):
    """
    inspired by https://github.com/invl/retry
    :param times: retry times
    :param delay: internals between each retry
    :param exceptions: exceptions may raise in retry
    :param logger: log for retry
    :return: func result or None
    """

    def _inter_retry(caller, retry_time, retry_delay, es):
        while retry_time:
            try:
                return caller()
            except es as e:
                retry_time -= 1
                if not retry_time:
                    logger.error("max tries for {} times, {} is raised, details: func name is {}, func args are {}".
                                 format(retry_time, e, caller.func.__name__, (caller.args, caller.keywords)))
                    raise
                time.sleep(retry_delay)

    def retry_oper(func):
        @wraps(func)
        def _wraps(*args, **kwargs):
            return _inter_retry(partial(func, *args, **kwargs), times, delay, exceptions)

        return _wraps

    return retry_oper

