#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import logging
import logging.config as log_conf


sys.path.append("../")
from utils.settings import ROOT_PATH

LOG_PATH = os.path.join(ROOT_PATH, 'logs')
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

LOG_FILE = os.path.join(LOG_PATH, 'wxb.log')

log_config = {
    'version': 1.0,
    'formatters': {
        'detail': {
            'format': '%(asctime)s - %(name)s  - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'detail'
        },
        'simple': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'filename': LOG_FILE,
            'level': 'INFO',
            'formatter': 'detail',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'crawler': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'other': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'storage': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
    }
}

log_conf.dictConfig(log_config)

crawler = logging.getLogger('crawler')
other = logging.getLogger('other')
storage = logging.getLogger('storage')