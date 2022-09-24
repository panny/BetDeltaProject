from django.db import models
import django.utils.timezone as timezone
from django.utils.html import format_html


# Create your models here.

class Field(models.Model):
    rank_tag = models.CharField(blank=True, null=True, max_length=100, verbose_name='自定义id')
    rank_mask = models.CharField(blank=True, null=True, max_length=100, verbose_name='赛场标记')
    rank_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='排位赛id')
    place = models.CharField(blank=True, null=True, max_length=100, verbose_name='比赛地')
    number = models.CharField(blank=True, null=True, max_length=100, verbose_name='场次')
    name = models.CharField(blank=True, null=True, max_length=100, verbose_name='赛事')
    rank_date = models.CharField(blank=True, null=True, max_length=100, verbose_name='日期')
    field = models.CharField(blank=True, null=True, max_length=100, verbose_name='场地')
    track = models.CharField(blank=True, null=True, max_length=100, verbose_name='赛道')
    route = models.CharField(blank=True, null=True, max_length=100, verbose_name='途程')
    site_condition = models.CharField(blank=True, null=True, max_length=100, verbose_name='場地狀況')
    reward = models.CharField(blank=True, null=True, max_length=100, verbose_name='奖金')
    score = models.CharField(blank=True, null=True, max_length=100, verbose_name='评分')
    race_class = models.CharField(blank=True, null=True, max_length=100, verbose_name='賽事班次')
    update_date = models.DateTimeField('最后修改日期', auto_now=True)
    create_date = models.DateTimeField('新增时间', default=timezone.now)

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        db_table = 'field'
        verbose_name = "排位场地"
        verbose_name_plural = verbose_name


class Rank(models.Model):
    rank_tag = models.CharField(blank=True, null=True, max_length=100, verbose_name='自定义id')
    rank_mask = models.CharField(blank=True, null=True, max_length=100, verbose_name='赛场标记')
    number = models.CharField(blank=True, null=True, max_length=100, verbose_name='马匹编号')
    performance = models.CharField(blank=True, null=True, max_length=100, verbose_name='6次近绩')
    horse = models.CharField(blank=True, null=True, max_length=100, verbose_name='马名')
    horse_no = models.CharField(blank=True, null=True, max_length=100, verbose_name='马no')
    stigma = models.CharField(blank=True, null=True, max_length=100, verbose_name='烙号')
    weight_bear = models.CharField(blank=True, null=True, max_length=100, verbose_name='负磅')
    jockey = models.CharField(blank=True, null=True, max_length=100, verbose_name='骑师')
    jockey_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='骑师id')
    is_over_weight = models.CharField(blank=True, null=True, max_length=100, verbose_name='可能超磅')
    position = models.CharField(blank=True, null=True, max_length=100, verbose_name='档位')
    trainer = models.CharField(blank=True, null=True, max_length=100, verbose_name='练马师')
    trainer_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='练师id')
    score = models.CharField(blank=True, null=True, max_length=100, verbose_name='评分')
    score_plus = models.CharField(blank=True, null=True, max_length=100, verbose_name='评分+')
    position_weight = models.CharField(blank=True, null=True, max_length=100, verbose_name='排位体重')
    position_weight_plus = models.CharField(blank=True, null=True, max_length=100, verbose_name='排位体重+')
    best_time = models.CharField(blank=True, null=True, max_length=100, verbose_name='最佳时间')
    horse_age = models.CharField(blank=True, null=True, max_length=100, verbose_name='马龄')
    horse_pound = models.CharField(blank=True, null=True, max_length=100, verbose_name='分龄让磅')
    sex = models.CharField(blank=True, null=True, max_length=100, verbose_name='性别')
    reward = models.CharField(blank=True, null=True, max_length=100, verbose_name='今季奖金')
    priority_order = models.CharField(blank=True, null=True, max_length=100, verbose_name='优先参赛次序')
    equipment = models.CharField(blank=True, null=True, max_length=100, verbose_name='配备')
    owner = models.CharField(blank=True, null=True, max_length=100, verbose_name='马主')
    father = models.CharField(blank=True, null=True, max_length=100, verbose_name='父系')
    mother = models.CharField(blank=True, null=True, max_length=100, verbose_name='母系')
    imported_type = models.CharField(blank=True, null=True, max_length=100, verbose_name='进口类别')
    classify = models.CharField(blank=True, null=True, max_length=100, verbose_name='赛马类别')
    update_date = models.DateTimeField('最后修改日期', auto_now=True)
    create_date = models.DateTimeField('新增时间', default=timezone.now)

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        db_table = 'rank'
        verbose_name = "排位赛"
        verbose_name_plural = verbose_name


class RankRecord(models.Model):
    rank_tag = models.CharField(blank=True, null=True, max_length=100, verbose_name='自定义id')
    rank_mask = models.CharField(blank=True, null=True, max_length=100, verbose_name='赛场标记')
    rank_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='排位赛id')
    order = models.CharField(blank=True, null=True, max_length=100, verbose_name='名次')
    number = models.CharField(blank=True, null=True, max_length=100, verbose_name='馬號')
    horse = models.CharField(blank=True, null=True, max_length=100, verbose_name='马名')
    horse_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='马id')
    horse_no = models.CharField(blank=True, null=True, max_length=100, verbose_name='马no')
    jockey = models.CharField(blank=True, null=True, max_length=100, verbose_name='騎師')
    jockey_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='騎師id')
    trainer = models.CharField(blank=True, null=True, max_length=100, verbose_name='練馬師')
    trainer_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='练师id')
    actual_pound = models.CharField(blank=True, null=True, max_length=100, verbose_name='實際負磅')
    position_weight = models.CharField(blank=True, null=True, max_length=100, verbose_name='排位體重')
    position = models.CharField(blank=True, null=True, max_length=100, verbose_name='檔位')
    head_distance = models.CharField(blank=True, null=True, max_length=100, verbose_name='頭馬距離')
    blocking = models.CharField(blank=True, null=True, max_length=100, verbose_name='沿途走位')
    finish_time = models.CharField(blank=True, null=True, max_length=100, verbose_name='完成时间')
    single_win = models.CharField(blank=True, null=True, max_length=100, verbose_name='獨贏賠率')
    update_date = models.DateTimeField('最后修改日期', auto_now=True)
    create_date = models.DateTimeField('新增时间', default=timezone.now)

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        db_table = 'rank_record'
        verbose_name = "排位赛果"
        verbose_name_plural = verbose_name


class Horse(models.Model):
    name = models.CharField(blank=True, null=True, max_length=100, verbose_name='马')
    horse_no = models.CharField(blank=True, null=True, max_length=100, verbose_name='马no')
    horse_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='马id')
    birth_place = models.CharField(blank=True, null=True, max_length=100, verbose_name='出生地')
    age = models.CharField(blank=True, null=True, max_length=100, verbose_name='馬齡')
    trainer = models.CharField(blank=True, null=True, max_length=100, verbose_name='練馬師')
    color = models.CharField(blank=True, null=True, max_length=100, verbose_name='毛色')
    sex = models.CharField(blank=True, null=True, max_length=100, verbose_name='性別')
    owner = models.CharField(blank=True, null=True, max_length=100, verbose_name='馬主')
    imported_type = models.CharField(blank=True, null=True, max_length=100, verbose_name='進口類別')
    current_score = models.CharField(blank=True, null=True, max_length=100, verbose_name='現時評分')
    reward = models.CharField(blank=True, null=True, max_length=100, verbose_name='今季獎金')
    season_score = models.CharField(blank=True, null=True, max_length=100, verbose_name='季初評分')
    reward_total = models.CharField(blank=True, null=True, max_length=100, verbose_name='總獎金')
    father = models.CharField(blank=True, null=True, max_length=100, verbose_name='父系')
    reward_times = models.CharField(blank=True, null=True, max_length=100, verbose_name='冠-亞-季-總出賽次數')
    mother = models.CharField(blank=True, null=True, max_length=100, verbose_name='母系')
    lately_rank = models.CharField(blank=True, null=True, max_length=100, verbose_name='最近十個賽馬日')
    grandfather = models.CharField(blank=True, null=True, max_length=100, verbose_name='外祖父')
    rank_times = models.CharField(blank=True, null=True, max_length=100, verbose_name='出賽場數')
    location = models.CharField(blank=True, null=True, max_length=100, verbose_name='現在位置')
    arrival_date = models.CharField(blank=True, null=True, max_length=100, verbose_name='到達日期')
    url = models.CharField(blank=True, null=True, max_length=200, verbose_name='链接')
    update_date = models.DateTimeField('最后修改日期', auto_now=True)
    create_date = models.DateTimeField('新增时间', default=timezone.now)

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        db_table = 'horse'
        verbose_name = "赛马"
        verbose_name_plural = verbose_name


class HorseRank(models.Model):
    name = models.CharField(blank=True, null=True, max_length=100, verbose_name='马')
    horse_no = models.CharField(blank=True, null=True, max_length=100, verbose_name='马no')
    horse_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='马编号')
    rank_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='場次')
    ranking = models.CharField(blank=True, null=True, max_length=100, verbose_name='名次')
    rank_date = models.CharField(blank=True, null=True, max_length=100, verbose_name='日期')
    track = models.CharField(blank=True, null=True, max_length=100, verbose_name='賽道')
    route = models.CharField(blank=True, null=True, max_length=100, verbose_name='途程')
    site_condition = models.CharField(blank=True, null=True, max_length=100, verbose_name='場地狀況')
    race_class = models.CharField(blank=True, null=True, max_length=100, verbose_name='賽事班次')
    position = models.CharField(blank=True, null=True, max_length=100, verbose_name='檔位')
    score = models.CharField(blank=True, null=True, max_length=100, verbose_name='評分')
    trainer = models.CharField(blank=True, null=True, max_length=100, verbose_name='練馬師')
    jockey = models.CharField(blank=True, null=True, max_length=100, verbose_name='騎師')
    trainer_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='练师id')
    jockey_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='騎師id')
    head_distance = models.CharField(blank=True, null=True, max_length=100, verbose_name='頭馬距離')
    single_win = models.CharField(blank=True, null=True, max_length=100, verbose_name='獨贏賠率')
    actual_pound = models.CharField(blank=True, null=True, max_length=100, verbose_name='實際負磅')
    blocking = models.CharField(blank=True, null=True, max_length=100, verbose_name='沿途走位')
    finish_time = models.CharField(blank=True, null=True, max_length=100, verbose_name='完成時間')
    position_weight = models.CharField(blank=True, null=True, max_length=100, verbose_name='排位體重')
    equipment = models.CharField(blank=True, null=True, max_length=100, verbose_name='配備')
    update_date = models.DateTimeField('最后修改日期', auto_now=True)
    create_date = models.DateTimeField('新增时间', default=timezone.now)

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        db_table = 'horse_rank'
        verbose_name = "赛马排位"
        verbose_name_plural = verbose_name


class Jockey(models.Model):
    jockey_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='骑师id')
    name = models.CharField(blank=True, null=True, max_length=100, verbose_name='姓名')
    age = models.CharField(blank=True, null=True, max_length=100, verbose_name='年龄')
    background = models.TextField(blank=True, null=True, max_length=2000, verbose_name='背景')
    achievement = models.TextField(blank=True, null=True, max_length=2000, verbose_name='成就')
    champion = models.TextField(blank=True, null=True, max_length=2000, verbose_name='賽事冠軍')
    head_horse = models.TextField(blank=True, null=True, max_length=2000, verbose_name='累積頭馬')
    country = models.CharField(blank=True, null=True, max_length=100, verbose_name='國籍')
    reward = models.CharField(blank=True, null=True, max_length=100, verbose_name='獎金')
    win_times = models.CharField(blank=True, null=True, max_length=100, verbose_name='10個賽馬日獲勝次數')
    avg_score = models.CharField(blank=True, null=True, max_length=100, verbose_name='10個賽馬日平均績分')
    first = models.CharField(blank=True, null=True, max_length=100, verbose_name='冠')
    second = models.CharField(blank=True, null=True, max_length=100, verbose_name='亞')
    third = models.CharField(blank=True, null=True, max_length=100, verbose_name='季')
    forth = models.CharField(blank=True, null=True, max_length=100, verbose_name='殿')
    rank_times = models.CharField(blank=True, null=True, max_length=100, verbose_name='總出賽次數')
    win_score = models.CharField(blank=True, null=True, max_length=100, verbose_name='勝出率')
    ten_rank_times = models.CharField(blank=True, null=True, max_length=100, verbose_name='出賽次數')
    ten_head_horse = models.CharField(blank=True, null=True, max_length=100, verbose_name='頭馬次數')
    ten_win_score = models.CharField(blank=True, null=True, max_length=100, verbose_name='勝出率')
    ten_position_times = models.CharField(blank=True, null=True, max_length=100, verbose_name='入位次數')
    ten_position_score = models.CharField(blank=True, null=True, max_length=100, verbose_name='入位率')
    url = models.CharField(blank=True, null=True, max_length=200, verbose_name='链接')
    update_date = models.DateTimeField('最后修改日期', auto_now=True)
    create_date = models.DateTimeField('新增时间', default=timezone.now)

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        db_table = 'jockey'
        verbose_name = "骑师"
        verbose_name_plural = verbose_name


class JockeyRecord(models.Model):
    jockey_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='骑师id')
    name = models.CharField(blank=True, null=True, max_length=100, verbose_name='姓名')
    rank_date = models.CharField(blank=True, null=True, max_length=100, verbose_name='日期')
    place = models.CharField(blank=True, null=True, max_length=100, verbose_name='比赛地')
    rank_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='場次')
    ranking = models.CharField(blank=True, null=True, max_length=100, verbose_name='名次')
    track = models.CharField(blank=True, null=True, max_length=100, verbose_name='賽道')
    route = models.CharField(blank=True, null=True, max_length=100, verbose_name='途程')
    race_class = models.CharField(blank=True, null=True, max_length=100, verbose_name='賽事班次')
    site_condition = models.CharField(blank=True, null=True, max_length=100, verbose_name='場地狀況')
    horse = models.CharField(blank=True, null=True, max_length=100, verbose_name='馬名')
    position = models.CharField(blank=True, null=True, max_length=100, verbose_name='檔位')
    score = models.CharField(blank=True, null=True, max_length=100, verbose_name='評分')
    trainer = models.CharField(blank=True, null=True, max_length=100, verbose_name='練馬師')
    trainer_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='练师id')
    horse_no = models.CharField(blank=True, null=True, max_length=100, verbose_name='马no')
    equipment = models.CharField(blank=True, null=True, max_length=100, verbose_name='配備')
    horse_weight = models.CharField(blank=True, null=True, max_length=100, verbose_name='馬匹體重')
    actual_pound = models.CharField(blank=True, null=True, max_length=100, verbose_name='實際負磅')
    update_date = models.DateTimeField('最后修改日期', auto_now=True)
    create_date = models.DateTimeField('新增时间', default=timezone.now)

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        db_table = 'jockey_record'
        verbose_name = "骑师记录"
        verbose_name_plural = verbose_name


class JockeyRank(models.Model):
    jockey_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='骑师id')
    name = models.CharField(blank=True, null=True, max_length=100, verbose_name='姓名')
    place = models.CharField(blank=True, null=True, max_length=100, verbose_name='比赛地')
    track = models.CharField(blank=True, null=True, max_length=100, verbose_name='賽道')
    route = models.CharField(blank=True, null=True, max_length=100, verbose_name='途程')
    first = models.CharField(blank=True, null=True, max_length=100, verbose_name='冠')
    second = models.CharField(blank=True, null=True, max_length=100, verbose_name='亞')
    third = models.CharField(blank=True, null=True, max_length=100, verbose_name='季')
    rank_times = models.CharField(blank=True, null=True, max_length=100, verbose_name='總出賽次數')
    update_date = models.DateTimeField('最后修改日期', auto_now=True)
    create_date = models.DateTimeField('新增时间', default=timezone.now)

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        db_table = 'jockey_rank'
        verbose_name = "骑师排位"
        verbose_name_plural = verbose_name


class Trainer(models.Model):
    trainer_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='练师id')
    name = models.CharField(blank=True, null=True, max_length=100, verbose_name='姓名')
    age = models.CharField(blank=True, null=True, max_length=100, verbose_name='年齡')
    background = models.TextField(blank=True, null=True, max_length=2000, verbose_name='背景')
    achievement = models.TextField(blank=True, null=True, max_length=2000, verbose_name='成就')
    champion = models.TextField(blank=True, null=True, max_length=2000, verbose_name='賽事冠軍')
    head_horse = models.TextField(blank=True, null=True, max_length=2000, verbose_name='累積頭馬')
    reward = models.CharField(blank=True, null=True, max_length=100, verbose_name='獎金')
    first = models.CharField(blank=True, null=True, max_length=100, verbose_name='冠')
    second = models.CharField(blank=True, null=True, max_length=100, verbose_name='亞')
    third = models.CharField(blank=True, null=True, max_length=100, verbose_name='季')
    rank_times = models.CharField(blank=True, null=True, max_length=100, verbose_name='總出賽次數')
    ten_rank_times = models.CharField(blank=True, null=True, max_length=100, verbose_name='出賽次數')
    ten_win_times = models.CharField(blank=True, null=True, max_length=100, verbose_name='勝出次數')
    ten_win_score = models.CharField(blank=True, null=True, max_length=100, verbose_name='勝出率')
    ten_position_times = models.CharField(blank=True, null=True, max_length=100, verbose_name='入位次數')
    ten_position_score = models.CharField(blank=True, null=True, max_length=100, verbose_name='入位率')
    url = models.CharField(blank=True, null=True, max_length=200, verbose_name='链接')
    update_date = models.DateTimeField('最后修改日期', auto_now=True)
    create_date = models.DateTimeField('新增时间', default=timezone.now)

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        db_table = 'trainer'
        verbose_name = "练师"
        verbose_name_plural = verbose_name


class TrainerRank(models.Model):
    trainer_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='练师id')
    name = models.CharField(blank=True, null=True, max_length=100, verbose_name='姓名')
    place = models.CharField(blank=True, null=True, max_length=100, verbose_name='比赛地')
    track = models.CharField(blank=True, null=True, max_length=100, verbose_name='賽道')
    route = models.CharField(blank=True, null=True, max_length=100, verbose_name='途程')
    first = models.CharField(blank=True, null=True, max_length=100, verbose_name='冠')
    second = models.CharField(blank=True, null=True, max_length=100, verbose_name='亞')
    third = models.CharField(blank=True, null=True, max_length=100, verbose_name='季')
    rank_times = models.CharField(blank=True, null=True, max_length=100, verbose_name='總出賽次數')
    update_date = models.DateTimeField('最后修改日期', auto_now=True)
    create_date = models.DateTimeField('新增时间', default=timezone.now)

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        db_table = 'trainer_rank'
        verbose_name = "练师排位"
        verbose_name_plural = verbose_name


class TrainerRecord(models.Model):
    trainer_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='骑师id')
    name = models.CharField(blank=True, null=True, max_length=100, verbose_name='姓名')
    rank_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='場次')
    horse = models.CharField(blank=True, null=True, max_length=100, verbose_name='馬名')
    ranking = models.CharField(blank=True, null=True, max_length=100, verbose_name='名次')
    rank_date = models.CharField(blank=True, null=True, max_length=100, verbose_name='日期')
    track = models.CharField(blank=True, null=True, max_length=100, verbose_name='賽道')
    route = models.CharField(blank=True, null=True, max_length=100, verbose_name='途程')
    site_condition = models.CharField(blank=True, null=True, max_length=100, verbose_name='場地狀況')
    position = models.CharField(blank=True, null=True, max_length=100, verbose_name='檔位')
    score = models.CharField(blank=True, null=True, max_length=100, verbose_name='評分')
    odds = models.CharField(blank=True, null=True, max_length=100, verbose_name='賠率')
    jockey = models.CharField(blank=True, null=True, max_length=100, verbose_name='騎師')
    horse_no = models.CharField(blank=True, null=True, max_length=100, verbose_name='马no')
    jockey_id = models.CharField(blank=True, null=True, max_length=100, verbose_name='騎師id')
    equipment = models.CharField(blank=True, null=True, max_length=100, verbose_name='配備')
    horse_weight = models.CharField(blank=True, null=True, max_length=100, verbose_name='馬匹體重')
    actual_pound = models.CharField(blank=True, null=True, max_length=100, verbose_name='實際負磅')
    first = models.CharField(blank=True, null=True, max_length=100, verbose_name='冠')
    second = models.CharField(blank=True, null=True, max_length=100, verbose_name='亞')
    third = models.CharField(blank=True, null=True, max_length=100, verbose_name='季')
    update_date = models.DateTimeField('最后修改日期', auto_now=True)
    create_date = models.DateTimeField('新增时间', default=timezone.now)

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        db_table = 'trainer_record'
        verbose_name = "练师记录"
        verbose_name_plural = verbose_name


class Task(models.Model):

    type_name = (
        ('0', '未处理'),
        ('1', '处理中'),
        ('2', '成功'),
        ('3', '失败'),
        ('4', '页面异常'),
    )

    task_id = models.CharField(blank=True, null=True, max_length=16, verbose_name='任务ID')
    name = models.CharField(blank=True, null=True, max_length=16, verbose_name='类型')
    spider = models.CharField(blank=True, null=True, max_length=32, verbose_name='爬取类')
    url = models.CharField(blank=True, null=True, max_length=200, verbose_name='链接')
    finish = models.CharField(default='0', choices=type_name, max_length=2, verbose_name="完成状态")
    tags = models.CharField(blank=True, null=True, max_length=16, verbose_name='批次')
    update_date = models.DateTimeField('最后修改日期', auto_now=True)
    create_date = models.DateTimeField('新增时间', default=timezone.now)

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        unique_together = (("url", "tags"),)
        db_table = 'task'
        verbose_name = "任务"
        verbose_name_plural = verbose_name


class TaskManager(models.Model):

    task_id = models.CharField(blank=True, null=True, max_length=16, verbose_name='任务ID')
    name = models.CharField(blank=True, null=True, max_length=16, verbose_name='类型')
    total = models.IntegerField(default=0, blank=True, null=True, verbose_name='任务总数')
    finish = models.IntegerField(default=0, blank=True, null=True, verbose_name='已完成')
    tags = models.CharField(blank=True, null=True, max_length=16, verbose_name='批次')
    update_date = models.DateTimeField('最后修改日期', auto_now=True)
    create_date = models.DateTimeField('新增时间', default=timezone.now)

    def percentage_paid(self):
        if self.finish and self.total:
            percentage = round((self.finish / self.total * 100), 2)
        else:
            percentage = 0
        return format_html(
            '''
            <progress value="{0}" max="100"></progress>
            <span style="font-weight:bold">{0}%</span>
            ''',
            percentage
        )

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        db_table = 'task_manager'
        verbose_name = "任务管理"
        verbose_name_plural = verbose_name
