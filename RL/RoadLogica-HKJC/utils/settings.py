#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
-------------------------------------------------------------------------------
    Name:         settings
    Description:  
    Email         wanglin1851@dingtalk.com
    Author:       Wang
    Time:         2019/11/25 18:23
-------------------------------------------------------------------------------
   Change Activity
                  2019/11/25 18:23
-------------------------------------------------------------------------------
"""
__author__ = 'Wang'

import os
import sys

sys.path.append("../")
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)

HORSE = {
    '出生地 / 馬齡': 'birth_place/age',
    '練馬師': 'trainer',
    '毛色 / 性別': 'color/sex',
    '馬主': 'owner',
    '進口類別': 'imported_type',
    '現時評分': 'current_score',
    '今季獎金*': 'reward',
    '季初評分': 'season_score',
    '總獎金*': 'reward_total',
    '父系': 'father',
    '冠-亞-季-總出賽次數*': 'reward_times',
    '母系': 'mother',
    '最近十個賽馬日': 'lately_rank',
    '最近十個賽馬日出賽場數': 'lately_rank',
    '外祖父': 'grandfather',
    '現在位置(到達日期)': 'location/arrival_date',
}

JOCKEY = {
    '年齡': 'age',
    '背景': 'background',
    '成就': 'achievement',
    '主要賽事冠軍': 'champion',
    '在港累積頭馬': 'head_horse',
    '國籍': 'country',
    '冠': 'first',
    '亞': 'second',
    '季': 'third',
    '殿': 'forth',
    '總出賽次數': 'rank_times',
    '勝出率': 'win_score',
    '所贏獎金': 'reward',
    '過去10個賽馬日獲勝次數': 'win_times',
    '過去10個賽馬日騎師王平均績分': 'avg_score',
}

PLACE = ['跑馬地', '沙田', '從化']

SAVE = {
    'field': {'url': 'http://127.0.0.1:8000/api/field/', "keys": ['rank_tag', 'rank_mask']},
    'rank': {'url': 'http://127.0.0.1:8000/api/rank/', "keys": ['rank_tag', 'horse']},
    'rank_record': {'url': 'http://127.0.0.1:8000/api/rank_record/', "keys": ['rank_tag', 'horse']},
    'horse': {'url': 'http://127.0.0.1:8000/api/horse/', "keys": ['horse_no', 'horse_id']},
    'horse_rank': {'url': 'http://127.0.0.1:8000/api/horse_rank/', "keys": ['horse_no', 'horse_id', 'rank_id']},
    'jockey': {'url': 'http://127.0.0.1:8000/api/jockey/', "keys": ['jockey_id']},
    'jockey_rank': {'url': 'http://127.0.0.1:8000/api/jockey_rank/', "keys": ['jockey_id', 'place', 'track', 'route']},
    'jockey_record': {'url': 'http://127.0.0.1:8000/api/jockey_record/', "keys": ['jockey_id', 'rank_id']},
    'trainer': {'url': 'http://127.0.0.1:8000/api/trainer/', "keys": ['trainer_id']},
    'trainer_rank': {'url': 'http://127.0.0.1:8000/api/trainer_rank/',
                     "keys": ['trainer_id', 'place', 'track', 'route']},
    'trainer_record': {'url': 'http://127.0.0.1:8000/api/trainer_record/', "keys": ['trainer_id', 'rank_id']},
}

HREF_RE = {
    r"horseno=(?P<HorseNo>[A-Z0-9]+)": {
        'url': 'https://racing.hkjc.com/racing/information/Chinese/Horse/Horse.aspx',
        'spider': 'Horse', 'name': '赛马'},
    r"JockeyId=(?P<JockeyId>[A-Z]+)": {
        'url': 'https://racing.hkjc.com/racing/information/Chinese/Jockey/JockeyWinStat.aspx',
        'spider': 'Jockey', 'name': '骑师'},
    r'TrainerCode=(?P<TrainerId>[A-Z]+)': {
        'url': 'https://racing.hkjc.com/racing/information/Chinese/Trainers/TrainerWinStat.aspx',
        'spider': 'Trainer', 'name': '练师'},
    r'jockeycode=(?P<JockeyId>[A-Z]+)': {
        'url': 'https://racing.hkjc.com/racing/information/Chinese/Jockey/JockeyWinStat.aspx',
        'spider': 'Jockey', 'name': '骑师'},
    r'trainercode=(?P<TrainerId>[A-Z]+)': {
        'url': 'https://racing.hkjc.com/racing/information/Chinese/Trainers/TrainerWinStat.aspx',
        'spider': 'Trainer', 'name': '练师'},
    r'/Local/(?P<tags>\d+)/(?P<place>[A-Z]+)/(?P<number>\d+)': {
        'url': 'https://racing.hkjc.com/racing/Info/meeting/RaceCard/chinese/Local/{tags}/{place}/{number}',
        'spider': 'Rank', 'name': '排位'},
    r'/Local/(?P<tags>\d+)/': {
        'url': 'https://racing.hkjc.com/racing/Info/meeting/RaceCard/chinese/Local/{tags}/',
        'spider': 'Rank', 'name': '排位'},
    r'RaceDate=(?P<RaceDate>[0-9\/]+)&Racecourse=(?P<Racecourse>[A-Z]+)&RaceNo=(?P<RaceNo>\d+)': {
        'url': 'https://racing.hkjc.com/racing/information/Chinese/Racing/LocalResults.aspx',
        'spider': 'RankRecord', 'name': '排位赛果'},
    r'RaceDate=(?P<RaceDate>[0-9\/]+)': {
        'url': 'https://racing.hkjc.com/racing/information/Chinese/Racing/LocalResults.aspx',
        'spider': 'RankRecord', 'name': '排位赛果'},
    r'racecard.aspx\?para=/(?P<para>[0-9A-Z\/]+)': {
        'url': 'https://racing.hkjc.com/racing/SystemDataPage/racing/overseas/RaceCard-SystemDataPage.aspx?match_id={para}/0&lang=Chinese',
        'spider': 'RankOversea', 'name': '海外排位'},
    r'results.aspx\?para=/(?P<para>[0-9A-Z\/]+)': {
        'url': 'https://racing.hkjc.com/racing/SystemDataPage/racing/overseas/Results-SystemDataPage.aspx?match_id={para}/0&lang=Chinese',
        'spider': 'RankRecordOversea', 'name': '海外赛果'},

}

SPIDER_UR = {
    'Horse': {'url': 'https://racing.hkjc.com/racing/information/Chinese/Horse/Horse.aspx', 'spider': 'Horse',
              'name': '赛马'},
    'Jockey': {'url': 'https://racing.hkjc.com/racing/information/Chinese/Jockey/JockeyWinStat.aspx',
               'spider': 'Jockey', 'name': '骑师'},
    'Trainer': {'url': 'https://racing.hkjc.com/racing/information/Chinese/Trainers/TrainerWinStat.aspx',
                'spider': 'Trainer', 'name': '练师'},
    'RankRecord': {'url': 'https://racing.hkjc.com/racing/information/Chinese/Racing/LocalResults.aspx',
                   'spider': 'RankRecord', 'name': '排位赛果'},
    'Rank': {
        'url': 'https://racing.hkjc.com/racing/Info/meeting/RaceCard/chinese/Local/', 'spider': 'Rank', 'name': '排位'},
    'RankOversea': {
        'url': 'https://racing.hkjc.com/racing/SystemDataPage/racing/overseas/RaceCard-SystemDataPage.aspx',
        'spider': 'RankOversea', 'name': '海外排位'},
    'RankRecordOversea': {
        'url': 'https://racing.hkjc.com/racing/SystemDataPage/racing/overseas/Results-SystemDataPage.aspx',
        'spider': 'RankRecord', 'name': '海外赛果'},
}

VAL_RE = {
    r'HorseId=([A-Z0-9_]+)': 'horse_id',
    r"horseno=([A-Z0-9]+)": 'horse_no',
    r"JockeyId=([A-Z]+)": 'jockey_id',
    r'TrainerId=([A-Z]+)': 'trainer_id',
    r'jockeycode=([A-Z]+)': 'jockey_id',
    r'trainercode=([A-Z]+)': 'trainer_id',
}

OverSea = ['20181125', '20190309', '20200307', '20190929', '20191124', '20191006', '20190519', '20190303', '20190601',
           '20190621', '20181014', '20191222', '20181007', '20181223', '20181106', '20190504', '20200328', '20190908',
           '20191019', '20200220', '20181111', '20190324', '20190221', '20190126', '20200201', '20191110', '20190623',
           '20190616', '20190512', '20190330', '20180930', '20191105', '20191013', '20180909', '20181027', '20190413',
           '20191027', '20190619', '20190525', '20181020']

pgs = {
    'host': '124.172.189.180',
    'port': 5432,
    'user': 'hkjc',
    'password': 'hkjc123456',
    'database': 'hkjc',
}
