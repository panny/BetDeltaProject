from django.db import models
import django.utils.timezone as timezone


# Create your models here.

class BetOdds(models.Model):
    rank_tag = models.CharField(blank=True, null=True, max_length=100, verbose_name='自定义id')
    date = models.DateTimeField(blank=True, null=True, verbose_name='比赛时间')
    venue = models.CharField(blank=True, null=True, max_length=100, verbose_name='比赛场地')
    raceno = models.IntegerField(default=1, verbose_name='比赛场次')
    number = models.IntegerField(default=1, verbose_name='马号')
    win = models.FloatField(default=999, verbose_name='獨贏')
    pla = models.FloatField(default=999, verbose_name='位置')
    create_date = models.DateTimeField('新增时间', default=timezone.now)

    def to_dict(self):
        data = {}
        for f in self._meta.concrete_fields:
            data[f.name] = f.value_from_object(self)
        return data

    class Meta:
        db_table = 'bet_odds'
        verbose_name = "赛马赔率"
        verbose_name_plural = verbose_name
