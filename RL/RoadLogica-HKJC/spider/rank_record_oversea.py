import re
import json
import furl
import time
import copy
from datetime import datetime
from lxml import etree

from spider.base import BaseSpider
from utils.httpclient import HttpClient
from utils.time import Time
from utils.settings import SAVE
from utils.config import Config
from utils.decorators import retry


class RankRecordOversea(BaseSpider):
    duplicates = []
    rank_tag = None
    rank_mask = None

    def duplicate(self):
        url = "http://127.0.0.1:8000/api/rank_record/?type=distinct&rank_mask=S1,S2"
        response = HttpClient.get(url=url)
        content = json.loads(response.text)
        if content.get('data'):
            self.duplicates = [x.get('rank_tag') for x in content.get('data')]
            self.duplicates = set(self.duplicates)

    def crawl(self):
        self.duplicate()
        if not self.content:
            response = HttpClient.get(self.session, url=self.url)
            self.content = response.text
        if self.info.get('flag'):
            find = re.findall(r'/racing/overseas/chinese/(\d+)/([A-Z0-9]+)/(\d+)/index.aspx', self.content)
            find = set(find)
            for f in find:
                rank_tag = f'{f [0]}{f [2]}'
                if f[0] < Time.get_format_time(t_format='%Y%m%d') and rank_tag not in self.duplicates:
                    url = f'/racing/overseas/Chinese/results.aspx?para=/{f[0]}/{f[1]}/{f[2]}'
                    self.href.append(url)
        else:
            args = furl.furl(self.url).args
            match_id = args.get('match_id')
            if match_id:
                find = re.search(r'(\d+)/([A-Z0-9]+)/(\d+)/', match_id)
                if find:
                    self.rank_tag = find.group(1) + find.group(3)
                    self.rank_mask = find.group(2)
                    self.single(self.content)
                    if find.group(3) == '1':
                        self.record(self.content)
        self.status = True

    def single(self, content):
        html = etree.HTML(content)
        trs = html.xpath("//table[@class='resultsTable draggable']/tr[@class]")
        data = []
        for tr in trs:
            text = []
            for x in tr.xpath('./td'):
                text.append(x.xpath('string(.)').replace('\r\n', '').strip())
            single = dict()
            single['rank_tag'] = self.rank_tag
            single['rank_mask'] = self.rank_mask
            single['order'] = text[0]
            single['number'] = text[2]
            single['horse'] = text[3]
            single['position'] = text[4]
            single['actual_pound'] = text[6]
            single['trainer'] = text[9]
            single['jockey'] = text[10]
            single['head_distance'] = text[11]
            single['single_win'] = text[12]
            data.append(single)
        self.result['rank_record'] = data

    def record(self, content):
        html = etree.HTML(content)
        hrefs = html.xpath("//div[@class='raceNum clearfix']//a[contains(@href, 'overseas')]/@href")
        for href in hrefs:
            find = re.search(r'(\d{8})/[A-Z0-9]+/(\d+)', href)
            if find:
                rank_tag = f"{find.group(1)}{find.group(2)}"
                if rank_tag not in self.duplicates:
                    self.href.append(href)

    @retry(times=3)
    def data_duplicate(self):
        tmp = {}
        for key, val in self.result.items():
            if isinstance(val, list) and key in SAVE:
                info = SAVE.get(key)
                response = HttpClient.get(url=info.get('url'), params={'rank_tag': self.rank_tag})
                content = response.json()
                if content.get('status') == '200' and content.get('data'):
                    data = Config.get_filter_dict(val, content.get('data'), info.get('keys'))
                else:
                    data = val
                tmp[key] = data
            else:
                tmp[key] = val
        self.result = tmp


if __name__ == '__main__':
    info = {'url': 'https://racing.hkjc.com/racing/SystemDataPage/racing/overseas/Results-SystemDataPage.aspx?match_id=20200704/S1/1/0&lang=Chinese',
            'task_id': '20200707', 'tags': '20200707'}
    rank = RankRecordOversea(**info)
    rank.get_data()
