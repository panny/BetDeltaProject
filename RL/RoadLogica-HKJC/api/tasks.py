#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import django
import traceback
import time
from celery import Celery
from celery.schedules import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hkjc.settings')
django.setup()
sys.path.append("../")
from api.models import Task
from utils.settings import SAVE
from utils.httpclient import HttpClient
from utils.instance import init_instance
from utils.time import TimeUnit, Time

app = Celery()
app.conf.update(
    BROKER_URL='redis://127.0.0.1:6379/1',
    CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/2',
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=False,
    CELERY_ACCEPT_CONTENT=['application/json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ACKS_LATE=False,
    CELERY_TASK_RESULT_EXPIRES=10 * 60,
    CELERYD_FORCE_EXECV=True,
    CELERYD_PREFETCH_MULTIPLIER=4,
    CELERYD_MAX_TASKS_PER_CHILD=200,
    CELERY_DISABLE_RATE_LIMITS=True,
    CELERY_DEFAULT_QUEUE='default',
    CELERY_DEFAULT_EXCHANGE='default',
    CELERY_DEFAULT_EXCHANGE_TYPE='direct',
    CELERY_DEFAULT_ROUTING_KEY='default',
    CELERY_TRACK_STARTED=True,
    CELERYBEAT_SCHEDULE={
        'spider_regular': {
            'task': 'api.tasks.spider_regular',
            'schedule': timedelta(seconds=10),
            'args': '',
        },
        'spider_redo': {
            'task': 'api.tasks.spider_redo',
            'schedule': timedelta(seconds=60),
            'args': '',
        },
    }
)


@app.task(queue='save')
def model_save(tb_name, data):
    if tb_name in SAVE:
        url = SAVE.get(tb_name).get("url")
        if isinstance(data, list):
            for dt in data:
                HttpClient.post(url=url, data=dt)
                time.sleep(2)
        else:
            HttpClient.post(url=url, data=data)
            time.sleep(2)


@app.task()
def spider_run(data):
    spider = init_instance('spider', data.get('spider'), **data)
    try:
        spider.get_data()
    except Exception as ex:
        print(ex, traceback.format_exc())


@app.task()
def spider_regular():
    task = Task.objects.filter(finish__in=['0', '3']).first()
    if task:
        task.finish = '1'
        task.save()
        info = {'url': task.url, 'task_id': task.task_id, 'tags': task.tags}
        spider = init_instance('spider', task.spider, **info)
        try:
            spider.get_data()
        except Exception as ex:
            print(ex, traceback.format_exc())
        url = "http://127.0.0.1:8000/api/manage/"
        HttpClient.post(url=url, data={'task_id': task.task_id})


@app.task()
def spider_redo():
    _time = Time.time_calculate(t_type=TimeUnit.MINUTE, num=-3)
    task = Task.objects.filter(finish__in='1', update_date__lt=_time).first()
    if task:
        info = {'url': task.url, 'task_id': task.task_id, 'tags': task.tags}
        spider = init_instance('spider', task.spider, **info)
        try:
            spider.get_data()
        except Exception as ex:
            print(ex, traceback.format_exc())
    url = "http://127.0.0.1:8000/api/manage/"
    HttpClient.post(url=url)
