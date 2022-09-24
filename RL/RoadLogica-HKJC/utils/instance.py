#!/usr/bin/python3
# -*- coding: utf-8 -*-
from enum import Enum
from spider import Rank, RankRecord, Trainer, Horse, Jockey, RankOversea, RankRecordOversea


def init_instance(module_name: str, class_name: str, *args, **kwargs):
    text = '{} {}'.format(class_name, kwargs)
    print(text)
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_meta, class_name)
    obj = class_meta(*args, **kwargs)
    return obj


class LazyProperty(object):
    """
    LazyProperty
    explain: http://www.spiderpy.cn/blog/5/
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


class Singleton(type):
    """
    Singleton Metaclass
    """

    _inst = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._inst:
            cls._inst[cls] = super(Singleton, cls).__call__(*args)
        return cls._inst[cls]


__all__ = ['init_instance', 'Singleton', 'LazyProperty']
